#!/usr/bin/python
"""
DataDog multi-step API synthetic test.

Replaces: New Relic Scripted API monitor (syntheticsCreateScriptApiMonitor,
          Node 16.10 runtime using $http.get/$http.post).

DataDog does not execute arbitrary Node.js, so the inline script stored in
the CSV Endpoint_Query column is parsed (best-effort, regex-based — not a
JS engine) into a single DataDog HTTP step:
  - method + url come from the first $http.get(...)/$http.post(...) call.
  - the POST body comes from that call's `json: {...}` options object,
    translated from a JS object literal into JSON.
  - `assert.equal(response.statusCode, <code>)` becomes the statusCode
    assertion (defaults to 200 if the script doesn't have one).
  - the rest of the $http callback's body-assertion logic becomes a single
    DataDog `javascript` assertion. DataDog's JS assertion sandbox exposes
    `dd.response.body` (raw string) and Chai's `assert` interface as
    `dd.assert` (whose `.ok`/`.equal`/`.match`/etc. mirror Node's built-in
    `assert` module). The callback body is carried over close to verbatim:
    `assert.` -> `dd.assert.`, and `const <body> = JSON.parse(dd.response.body);`
    is injected so the rest of the original code (property checks, regex
    matches, Array.isArray, etc.) keeps working unmodified. Any named helper
    function the script defines outside the callback (e.g. a `parseJson`
    wrapper) is carried over too, since the callback may call it.

This assumes each script has exactly one anonymous `$http` callback function
(true for every script in both CSVs today) and that `response.statusCode`
assertions are the only per-response detail used outside the callback body,
since DataDog's JS assertion sandbox doesn't expose the status code — that
line is dropped from the JS assertion and handled by the separate statusCode
assertion instead. Scripts that don't match these patterns are only
partially translated — anything left over is logged so it can be reviewed
manually.

Runs every 10 min (prod) or 30 min (other tiers).
"""

import json
import re

from monitors import dd_client
from monitors.synthetics.script_parsing import extract_balanced_braces


_HTTP_CALL_STRING_RE = re.compile(
    r"\$http\.(get|post|put|delete)\s*\(\s*"
    r"(?:'(?P<url_sq>[^']*)'|\"(?P<url_dq>[^\"]*)\")",
    re.IGNORECASE,
)
# $http.get({ url: url, timeout: 30000 }, ...) — url given as an options-object key,
# either a string literal directly or an identifier resolved via _STRING_ASSIGN_RE.
_HTTP_CALL_OPTS_RE = re.compile(
    r"\$http\.(get|post|put|delete)\s*\(\s*\{[^}]*?\burl\s*:\s*"
    r"(?:'(?P<url_sq>[^']*)'|\"(?P<url_dq>[^\"]*)\"|(?P<url_var>\w+))",
    re.IGNORECASE | re.DOTALL,
)
_STRING_ASSIGN_RE = re.compile(
    r"(?:const|let|var)\s+(\w+)\s*=\s*(?:'([^']*)'|\"([^\"]*)\")\s*;"
)
_STATUS_RE = re.compile(r"assert\.equal\(\s*response\.statusCode\s*,\s*(\d+)")
# A named top-level helper function the script defines and calls from inside
# its $http callback (e.g. DCC's `function parseJson(body) {...}`).
_HELPER_FUNC_RE = re.compile(r"function\s+\w+\s*\([^)]*\)\s*\{")
# The anonymous $http callback: function (err, response, body) {...}. Every
# script in both CSVs has exactly one anonymous function — the callback — so
# the last match in the script reliably identifies it.
_CALLBACK_RE = re.compile(
    r"function\s*\(\s*(\w+)(?:\s*,\s*(\w+))?(?:\s*,\s*(\w+))?\s*\)\s*\{"
)
_ERR_CHECK_RE = re.compile(r"if\s*\(\s*\w+\s*\)\s*(?:\{[^{}]*\}|[^;{}]*;)")
_CONSOLE_LOG_RE = re.compile(r"console\.log\([^;]*\);")
_STATUS_ASSERT_LINE_RE = re.compile(r"assert\.equal\(\s*response\.statusCode[^;]*;")
_ASSERT_CALL_RE = re.compile(r"\bassert\.")
_JSON_BLOCK_RE = re.compile(r"json\s*:\s*\{")
_BARE_KEY_RE = re.compile(r"(?<=[{,\s])(\w+)\s*:")
_SQ_STRING_RE = re.compile(r"'((?:[^'\\]|\\.)*)'")


def _parse_request(script):
    """Return (method, url) from the first $http.<method>(...) call, or (None, None)."""
    script = script or ""

    match = _HTTP_CALL_STRING_RE.search(script)
    if match:
        url = match.group("url_sq")
        if url is None:
            url = match.group("url_dq")
        return match.group(1).upper(), url

    match = _HTTP_CALL_OPTS_RE.search(script)
    if match:
        method = match.group(1).upper()
        url = match.group("url_sq") or match.group("url_dq")
        if url is None and match.group("url_var"):
            string_vars = {
                name: sq or dq for name, sq, dq in _STRING_ASSIGN_RE.findall(script)
            }
            url = string_vars.get(match.group("url_var"))
        return method, url

    return None, None


def _parse_status_code(script):
    match = _STATUS_RE.search(script or "")
    return int(match.group(1)) if match else 200


def _extract_helper_functions(script):
    """Return the full source text of every named top-level helper function."""
    helpers = []
    for match in _HELPER_FUNC_RE.finditer(script):
        text = extract_balanced_braces(script, match.end() - 1)
        if text:
            helpers.append(script[match.start() : match.start() + len(match.group()) - 1 + len(text)])
    return helpers


def _parse_js_assertion(script):
    """
    Translate the $http callback's body-assertion logic into a single DataDog
    `javascript` assertion, preserving the original checks close to verbatim.
    Returns {"type": "javascript", "code": ...} or None if nothing is left to
    assert after stripping the error check, logging, and statusCode line.
    """
    script = script or ""

    callback_match = None
    for match in _CALLBACK_RE.finditer(script):
        callback_match = match  # the $http callback is the last anonymous function
    if callback_match is None:
        return None

    body_text = extract_balanced_braces(script, callback_match.end() - 1)
    if body_text is None:
        return None
    inner = body_text[1:-1]

    inner = _ERR_CHECK_RE.sub("", inner)
    inner = _CONSOLE_LOG_RE.sub("", inner)
    inner = _STATUS_ASSERT_LINE_RE.sub("", inner)
    inner = inner.strip()
    if not inner:
        return None

    lines = _extract_helper_functions(script)
    body_param = callback_match.group(3)
    if body_param:
        lines.append("const {} = JSON.parse(dd.response.body);".format(body_param))
    lines.append(inner)

    code = _ASSERT_CALL_RE.sub("dd.assert.", "\n".join(lines))
    return {"type": "javascript", "code": code}


def _js_object_literal_to_json(js_obj):
    """
    Best-effort conversion of a simple JS object literal (bare keys,
    single-quoted strings) into a JSON string. Returns None if the result
    isn't valid JSON.
    """
    quoted_keys = _BARE_KEY_RE.sub(r'"\1":', js_obj)
    double_quoted = _SQ_STRING_RE.sub(lambda m: json.dumps(m.group(1)), quoted_keys)
    try:
        return json.dumps(json.loads(double_quoted))
    except ValueError:
        return None


def _parse_post_body(script):
    """
    Best-effort extraction of the `json: {...}` options object passed to
    $http.post(...), converted to a JSON string. Returns "" if none is
    found or it can't be parsed.
    """
    script = script or ""
    marker = _JSON_BLOCK_RE.search(script)
    if not marker:
        return ""

    js_obj = extract_balanced_braces(script, marker.end() - 1)
    if js_obj is None:
        return ""

    body = _js_object_literal_to_json(js_obj)
    return body or ""


def setmonitor(project, tier, api, notification):
    monitor_name = "{} {} {} Monitor".format(project, tier, api["name"])
    freq = dd_client.tick_every(tier)
    locations = dd_client.synthetics_location(api["location"])

    script = api["query"]
    method, parsed_url = _parse_request(script)
    if method is None:
        print(
            "WARNING: {}: no $http.get/post/put/delete(...) call found in "
            "Endpoint_Query; defaulting to GET {}.".format(monitor_name, api["url"])
        )
        method = "GET"
    request = {
        "method": method,
        "url": parsed_url or api["url"],
        "headers": {"Content-Type": "application/json"},
    }

    if method == "POST":
        body = _parse_post_body(script)
        if not body:
            print(
                "WARNING: {}: could not extract a POST body from "
                "Endpoint_Query; sending an empty body.".format(monitor_name)
            )
        request["body"] = body

    assertions = [
        {"operator": "is", "type": "statusCode", "target": _parse_status_code(script)},
    ]
    js_assertion = _parse_js_assertion(script)
    if js_assertion:
        assertions.append(js_assertion)

    print("{}: request being sent to DataDog:".format(monitor_name))
    print(json.dumps(request, indent=2))
    print("{}: assertions being sent to DataDog:".format(monitor_name))
    print(json.dumps(assertions, indent=2))

    description_fmt = {
        "name": api["name"],
        "tier": tier,
        "method": method,
        "url": request["url"],
    }

    payload = {
        "config": {
            "steps": [
                {
                    "name": "API check",
                    "subtype": "http",
                    "request": request,
                    "assertions": assertions,
                }
            ]

        },
        "locations": locations,
        "message": dd_client.build_alarm_message(
            locations,
            (
                "CRITICAL: The %(name)s endpoint in %(tier)s tier is failing its synthetic "
                "API check (%(method)s %(url)s). This indicates the endpoint is returning an "
                "unexpected status code or failing response validation, meaning the service "
                "may be unavailable or misbehaving."
            ) % description_fmt,
            (
                "RESOLVED: The %(name)s endpoint in %(tier)s tier has recovered and is "
                "passing its synthetic API check (%(method)s %(url)s)."
            ) % description_fmt,
            notification,
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
        },
        "status": "live",
        "tags": dd_client.default_tags(project, tier),
        "type": "api",
        "subtype": "multi",
    }

    return dd_client.upsert_and_report(monitor_name, "api", payload)
