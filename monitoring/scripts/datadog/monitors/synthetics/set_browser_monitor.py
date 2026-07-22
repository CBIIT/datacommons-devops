#!/usr/bin/python
"""
DataDog Browser synthetic test.

Replaces: New Relic Scripted Browser monitor (syntheticsCreateScriptBrowserMonitor,
          Chrome 100 runtime, WebDriver-style $browser/$driver script).

DataDog browser tests use a declarative "steps" array, not free-form
JavaScript. This module builds a single assertElementContent step from
whichever of two sources the CSV row provides:

Mode A — Browser_Query is set: the script is parsed (best-effort,
regex-based — not a JS engine):
  - the start URL comes from CONFIG.URL (falls back to the row's URL column).
  - the element locator comes from CONFIG.XPATH, passed to DataDog as a
    userLocator (the hand-specified locator format — DataDog's recorder-only
    multiLocator format can't be fabricated without a live browser session).
  - the wait timeout comes from the $driver.waitForAndFindElement(...) call's
    millisecond argument (default 20000ms if absent), converted to seconds.
This assumes the script has exactly one CONFIG block, one
waitForAndFindElement(...) call, and an xpath-based locator — true for
every Browser_Query in both CSVs today. Scripts that don't match (multiple
waits, non-xpath locators, no CONFIG block) are only partially translated:
a URL-only browser test is created (no content assertion) and a WARNING is
logged so it can be reviewed manually, rather than silently fabricating an
assertion that doesn't reflect the original script.

Mode B — Browser_Query is empty but Validation_Text is set: some pages
(e.g. JS-rendered SPAs) have no script at all in the CSV, only a validation
string, and a raw HTTP body-contains check can't see JS-rendered content.
The URL comes straight from the row's URL column, the locator is a default
XPath `//*[contains(text(), '<Validation_Text>')]`, and the timeout
defaults to 20 seconds.

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


_CONFIG_BLOCK_RE = re.compile(r"CONFIG\s*=\s*\{")
_CONFIG_URL_RE = re.compile(r"URL\s*:\s*(?:'([^']*)'|\"([^\"]*)\")")
_CONFIG_XPATH_RE = re.compile(r"XPATH\s*:\s*(?:'([^']*)'|\"([^\"]*)\")")
_CONFIG_EXPECTED_TEXT_RE = re.compile(r"EXPECTED_TEXT\s*:\s*(?:'([^']*)'|\"([^\"]*)\")")
_XPATH_CONTAINS_TEXT_RE = re.compile(
    r"contains\(\s*text\(\)\s*,\s*(?:'([^']*)'|\"([^\"]*)\")\s*\)"
)
_WAIT_CALL_RE = re.compile(r"waitForAndFindElement\([^,]+,\s*(\d+)\s*\)")
_XPATH_LOCATOR_RE = re.compile(r"\$driver\.By\.xpath\(")


def _extract_balanced_braces(text, open_brace_index):
    """Return the substring from open_brace_index through its matching '}'."""
    depth = 0
    for i in range(open_brace_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace_index : i + 1]
    return None


def _first_group(match):
    return match.group(1) if match.group(1) is not None else match.group(2)


def _parse_browser_check(script):
    """
    Parse a Browser_Query script into {"url", "xpath", "script_assert_text",
    "timeout_s"}, or None if it doesn't match the supported CONFIG +
    single-wait + xpath-locator shape. "script_assert_text" may itself be
    None if the script has no derivable expected text (e.g. no
    CONFIG.EXPECTED_TEXT and no contains(text(), ...) literal in the XPath)
    — callers should fall back to the CSV's Validation_Text in that case.
    """
    script = script or ""

    config_marker = _CONFIG_BLOCK_RE.search(script)
    if not config_marker:
        return None
    config_block = _extract_balanced_braces(script, config_marker.end() - 1)
    if config_block is None:
        return None

    url_match = _CONFIG_URL_RE.search(config_block)
    xpath_match = _CONFIG_XPATH_RE.search(config_block)
    if not url_match or not xpath_match:
        return None
    url = _first_group(url_match)
    xpath = _first_group(xpath_match)

    # Only a single wait + an xpath-based locator is supported; anything
    # more complex (multiple waits, CSS/id locators, conditional logic)
    # isn't safely translatable without misrepresenting the original check.
    wait_calls = _WAIT_CALL_RE.findall(script)
    if len(wait_calls) != 1 or not _XPATH_LOCATOR_RE.search(script):
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
    xpath = "//*[contains(text(), {})]".format(_xpath_string_literal(validation_text))
    return {
        "url": url,
        "xpath": xpath,
        "script_assert_text": None,
        "timeout_s": 20,
    }


def setmonitor(project, tier, api, notification):
    monitor_name = "{} {} {} Monitor".format(project, tier, api["name"])
    freq = 600 if tier.lower() == "prod" else 1800  # seconds
    locations = dd_client.synthetics_location(api["location"])

    browser_query = (api.get("browser_query") or "").strip()
    validation_text = (api.get("text") or "").strip()

    if browser_query:
        parsed = _parse_browser_check(browser_query)  # Mode A
    elif validation_text:
        parsed = _default_browser_check(api["url"], validation_text)  # Mode B
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
                                "values": [
                                    {"type": "xpath", "value": parsed["xpath"]},
                                ],
                            },
                        },
                    },
                }
            )

    payload = {
        "config": {
            "assertions": [],
            "request": {
                "headers": {},
                "method": "GET",
                "url": (parsed["url"] if parsed else None) or api["url"],
            },
            "setCookie": "",
            "variables": [],
        },
        "steps": steps,
        "locations": locations,
        "message": "{} {} {} browser check failed.\n{}".format(
            project, tier, api["name"], notification
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
            "device_ids": ["laptop_large"],
        },
        "status": "live",
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "type": "browser",
    }

    public_id = dd_client.find_synthetic_test(monitor_name)
    if public_id:
        print("{} already exists, updating with latest configuration.".format(monitor_name))
    else:
        print("{} not found, creating.".format(monitor_name))

    public_id = dd_client.upsert_synthetic_test(public_id, "browser", payload)
    print("{} upserted (public_id: {}).".format(monitor_name, public_id))
    return public_id
