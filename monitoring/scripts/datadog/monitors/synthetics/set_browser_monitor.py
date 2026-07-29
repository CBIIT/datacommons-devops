#!/usr/bin/python

"""

DataDog Browser synthetic test.



Replaces: New Relic Scripted Browser monitor (syntheticsCreateScriptBrowserMonitor,

          Chrome 100 runtime, WebDriver-style $browser/$driver script).



DataDog browser tests use a declarative "steps" array, not free-form

JavaScript. This module builds an assertion step from whichever of two

sources the CSV row provides:



Mode A — Browser_Query is set: the script is parsed (best-effort,

regex-based — not a JS engine):

  - the start URL comes from CONFIG.URL (falls back to the row's URL column).

  - the element locator comes from CONFIG.XPATH, passed to DataDog as a

    userLocator (the hand-specified locator format — DataDog's recorder-only

    multiLocator format can't be fabricated without a live browser session).

  - the wait timeout comes from the $driver.waitForAndFindElement(...) call's

    millisecond argument (default 20000ms if absent), converted to seconds.

  - if the script also sets CONFIG.DISMISS_XPATH and calls .click() on the

    element found via that locator (e.g. dismissing a consent/warning modal

    that would otherwise leave the target element present-but-invisible —

    DataDog's assertElementContent fails with "Element located but it's

    invisible" in that case), a "click" step is inserted before the

    assertElementContent step to dismiss it first.

This assumes the script has exactly one CONFIG block, and either one

waitForAndFindElement(...) call (no dismiss step), or exactly two — the

first for CONFIG.DISMISS_XPATH followed by .click(), the second for

CONFIG.XPATH — and an xpath-based locator throughout. Scripts that don't

match (more waits, non-xpath locators, no CONFIG block, a DISMISS_XPATH

with no matching .click()) are only partially translated: a URL-only

browser test is created (no content assertion) and a WARNING is logged so

it can be reviewed manually, rather than silently fabricating an assertion

that doesn't reflect the original script.



Mode B — Browser_Query is empty but Validation_Text is set: some pages

(e.g. JS-rendered SPAs) have no script at all in the CSV, only a validation

string, and a raw HTTP body-contains check can't see JS-rendered content.

The URL comes straight from the row's URL column, the locator is a default

XPath `//*[contains(text(), '<Validation_Text>')]`, and the timeout

defaults to 20 seconds. Since there's no script, this is just a "does the

page contain this text" check (matching New Relic's plain validation) —

translated as an assertElementPresent step rather than assertElementContent,

since presence doesn't require the element to be visible (assertElementContent

does, and fails with "Element located but it's invisible" for text that's

present but currently hidden behind e.g. a consent modal — a real failure

mode hit on a page with no dismiss mechanism in either New Relic's original

config or this CSV). The "contains text" condition is encoded directly in

the XPath, since assertElementPresent takes no separate check/value.



In both modes, the assertion text prefers the CSV's Validation_Text column

when it's set (the same human-curated, authoritative field

set_api_http_monitor.py already treats as the source of truth for its

body-contains checks). Only when Validation_Text is blank does Mode A fall

back to text derived from the script itself: the case-exact literal

embedded in the XPath's own contains(text(), '<literal>') clause, then

CONFIG.EXPECTED_TEXT. The XPath literal is preferred over EXPECTED_TEXT

because the original script lowercases EXPECTED_TEXT before comparing

(`.toLowerCase().includes(...)`) but DataDog's `contains` operator is

case-sensitive — reusing EXPECTED_TEXT verbatim would likely fail the same

way a case-sensitive body-contains check just failed elsewhere.



Runs every 10 min (prod) or 30 min (other tiers).

"""



import re



from monitors import dd_client

from monitors.synthetics.script_parsing import extract_balanced_braces





_CONFIG_BLOCK_RE = re.compile(r"CONFIG\s*=\s*\{")

_CONFIG_URL_RE = re.compile(r"URL\s*:\s*(?:'([^']*)'|\"([^\"]*)\")")

_CONFIG_XPATH_RE = re.compile(r"(?<![_A-Za-z])XPATH\s*:\s*(?:'([^']*)'|\"([^\"]*)\")")

_CONFIG_EXPECTED_TEXT_RE = re.compile(r"EXPECTED_TEXT\s*:\s*(?:'([^']*)'|\"([^\"]*)\")")

_CONFIG_DISMISS_XPATH_RE = re.compile(r"DISMISS_XPATH\s*:\s*(?:'([^']*)'|\"([^\"]*)\")")

_XPATH_CONTAINS_TEXT_RE = re.compile(

    r"contains\(\s*text\(\)\s*,\s*(?:'([^']*)'|\"([^\"]*)\")\s*\)"

)

_WAIT_CALL_RE = re.compile(r"waitForAndFindElement\([^,]+,\s*(\d+)\s*\)")

_XPATH_LOCATOR_RE = re.compile(r"\$driver\.By\.xpath\(")

_CLICK_CALL_RE = re.compile(r"\.click\(\s*\)")





def _first_group(match):

    return match.group(1) if match.group(1) is not None else match.group(2)





def _parse_browser_check(script):

    """

    Parse a Browser_Query script into {"url", "xpath", "script_assert_text",

    "timeout_s", "dismiss_xpath", "dismiss_timeout_s"}, or None if it

    doesn't match the supported CONFIG + wait(s) + xpath-locator shape.

    "script_assert_text" may itself be None if the script has no derivable

    expected text (e.g. no CONFIG.EXPECTED_TEXT and no contains(text(), ...)

    literal in the XPath) — callers should fall back to the CSV's

    Validation_Text in that case. "dismiss_xpath"/"dismiss_timeout_s" are

    None unless the script sets CONFIG.DISMISS_XPATH and clicks it (e.g. to

    dismiss a consent/warning modal) before waiting on CONFIG.XPATH.

    """

    script = script or ""



    config_marker = _CONFIG_BLOCK_RE.search(script)

    if not config_marker:

        return None

    config_block = extract_balanced_braces(script, config_marker.end() - 1)

    if config_block is None:

        return None



    url_match = _CONFIG_URL_RE.search(config_block)

    xpath_match = _CONFIG_XPATH_RE.search(config_block)

    if not url_match or not xpath_match:

        return None

    url = _first_group(url_match)

    xpath = _first_group(xpath_match)



    dismiss_match = _CONFIG_DISMISS_XPATH_RE.search(config_block)

    dismiss_xpath = _first_group(dismiss_match) if dismiss_match else None



    wait_calls = _WAIT_CALL_RE.findall(script)

    if not _XPATH_LOCATOR_RE.search(script):

        return None



    dismiss_timeout_s = None

    if dismiss_xpath:

        # Dismiss step present: expect exactly two waits (dismiss, then

        # target) and a .click() call to actually dismiss the interstitial

        # — otherwise this isn't safely translatable, so bail rather than

        # guess which wait is which.

        if len(wait_calls) != 2 or not _CLICK_CALL_RE.search(script):

            return None

        dismiss_timeout_s = max(1, round(int(wait_calls[0]) / 1000))

        timeout_s = max(1, round(int(wait_calls[1]) / 1000))

    else:

        # Only a single wait + an xpath-based locator is supported; anything

        # more complex (multiple waits, CSS/id locators, conditional logic)

        # isn't safely translatable without misrepresenting the original check.

        if len(wait_calls) != 1:

            return None

        timeout_s = max(1, round(int(wait_calls[0]) / 1000))



    contains_match = _XPATH_CONTAINS_TEXT_RE.search(xpath)

    if contains_match:

        script_assert_text = _first_group(contains_match)

    else:

        expected_match = _CONFIG_EXPECTED_TEXT_RE.search(config_block)

        script_assert_text = _first_group(expected_match) if expected_match else None



    return {

        "url": url,

        "xpath": xpath,

        "script_assert_text": script_assert_text,

        "timeout_s": timeout_s,

        "dismiss_xpath": dismiss_xpath,

        "dismiss_timeout_s": dismiss_timeout_s,

    }





def _xpath_string_literal(text):

    """XPath string literal for `text`, handling embedded quotes via concat()."""

    if "'" not in text:

        return "'{}'".format(text)

    if '"' not in text:

        return '"{}"'.format(text)

    # XPath 1.0 has no escape character, so a literal containing both quote

    # types has to be built as concat('part', "'", 'part', "'", ...).

    parts = text.split("'")

    pieces = []

    for i, part in enumerate(parts):

        if part:

            pieces.append("'{}'".format(part))

        if i != len(parts) - 1:

            pieces.append("\"'\"")

    return "concat({})".format(", ".join(pieces))





def _default_browser_check(url, validation_text):

    """Mode B: no Browser_Query, build a check straight from Validation_Text."""

    # Real pages frequently contain more than one element with the same

    # text (e.g. a duplicate nav item hidden behind a mobile/hamburger

    # menu), and DataDog's userLocator errors ("Multiple elements found")

    # if the XPath doesn't resolve to exactly one node -- so pin to the

    # first match rather than leaving the locator ambiguous.

    xpath = "(//*[contains(text(), {})])[1]".format(_xpath_string_literal(validation_text))

    return {

        "url": url,

        "xpath": xpath,

        "script_assert_text": None,

        "timeout_s": 20,

        "dismiss_xpath": None,

        "dismiss_timeout_s": None,

    }





def setmonitor(project, tier, api, notification):

    monitor_name = "{} {} {} Monitor".format(project, tier, api["name"])

    freq = dd_client.tick_every(tier)

    locations = dd_client.synthetics_location(api["location"])



    browser_query = (api.get("browser_query") or "").strip()

    validation_text = (api.get("text") or "").strip()



    mode_b = False

    if browser_query:

        parsed = _parse_browser_check(browser_query)  # Mode A

    elif validation_text:

        parsed = _default_browser_check(api["url"], validation_text)  # Mode B

        mode_b = True

    else:

        parsed = None



    steps = []

    if parsed is None:

        print(

            "WARNING: {}: no Browser_Query or Validation_Text produced a "

            "usable wait-for-element + assert-text check; creating a "

            "URL-only browser test with no content assertion.".format(monitor_name)

        )

    else:

        assert_text = validation_text or parsed["script_assert_text"]

        if not assert_text:

            print(

                "WARNING: {}: found a URL/element locator in Browser_Query "

                "but no expected text (Validation_Text is blank and the "

                "script has no derivable text); creating a browser test "

                "with no content assertion.".format(monitor_name)

            )

        else:

            if parsed.get("dismiss_xpath"):

                steps.append(

                    {

                        "name": "Dismiss interstitial",

                        "type": "click",

                        "timeout": parsed["dismiss_timeout_s"],

                        "isCritical": True,

                        "params": {

                            "element": {

                                "userLocator": {

                                    "failTestOnCannotLocate": True,

                                    "values": [

                                        {"type": "xpath", "value": parsed["dismiss_xpath"]},

                                    ],

                                },

                            },

                        },

                    }

                )

            if mode_b:

                # Mode B has no script -- it's a plain "does this text exist

                # on the page" check, same as New Relic's simple validation.

                # assertElementContent requires the element to be visible

                # (fails "Element located but it's invisible" behind e.g. a

                # consent modal); assertElementPresent only requires DOM

                # presence, which is what a plain text-contains check should

                # actually mean, and matches New Relic's behavior here. The

                # "contains text" condition is already encoded in the XPath.

                steps.append(

                    {

                        "name": "Assert element present",

                        "type": "assertElementPresent",

                        "timeout": parsed["timeout_s"],

                        "isCritical": True,

                        "params": {

                            "element": {

                                "userLocator": {

                                    "failTestOnCannotLocate": True,

                                    "values": [

                                        {"type": "xpath", "value": parsed["xpath"]},

                                    ],

                                },

                            },

                        },

                    }

                )

            else:

                # Mode A scripts call .getText() on the located element,

                # which (like real Selenium/WebDriver) only returns text for

                # visible elements -- assertElementContent's visibility

                # requirement is the faithful translation of that behavior.

                steps.append(

                    {

                        "name": "Assert element text",

                        "type": "assertElementContent",

                        "timeout": parsed["timeout_s"],

                        "isCritical": True,

                        "params": {

                            "check": "contains",

                            "value": assert_text,

                            "element": {

                                "userLocator": {

                                    "failTestOnCannotLocate": True,

                                    "values": [

                                        {"type": "xpath", "value": parsed["xpath"]},

                                    ],

                                },

                            },

                        },

                    }

                )



    resolved_url = (parsed["url"] if parsed else None) or api["url"]

    description_fmt = {"name": api["name"], "tier": tier, "url": resolved_url}



    payload = {

        "config": {

            "assertions": [],

            "request": {

                "headers": {},

                "method": "GET",

                "url": resolved_url,

            },

            "setCookie": "",

            "variables": [],

        },

        "steps": steps,

        "locations": locations,

        "message": dd_client.build_alarm_message(

            locations,

            (

                "CRITICAL: The %(name)s endpoint in %(tier)s tier is failing its synthetic "

                "browser check (%(url)s). This indicates the expected element/content could "

                "not be found on the rendered page, meaning the service may be unavailable or "

                "misbehaving."

            ) % description_fmt,

            (

                "RESOLVED: The %(name)s endpoint in %(tier)s tier has recovered and is "

                "passing its synthetic browser check (%(url)s)."

            ) % description_fmt,

            notification,

        ),

        "name": monitor_name,

        "options": {

            "tick_every": freq,

            "device_ids": ["laptop_large"],

        },

        "status": "live",

        "tags": dd_client.default_tags(project, tier),

        "type": "browser",

    }



    return dd_client.upsert_and_report(monitor_name, "browser", payload)