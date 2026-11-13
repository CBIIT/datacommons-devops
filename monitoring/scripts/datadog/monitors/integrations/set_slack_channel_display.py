#!/usr/bin/python
"""
Hide the "Tags" section in Datadog's Slack alerts.

The Tags section comes from the Datadog Slack integration's per-channel
display setting, not from the monitor message. For each Slack channel our
monitors notify, this sets display.tags = false and keeps every other
display setting as it is.

CSV Slack_Channel values are "<account>-<channel>" (the part after "@slack-"
in the handle), e.g. "Expand_Data_Commons-ccdi-subprod-cbio" -> account
"Expand_Data_Commons", channel "#ccdi-subprod-cbio". Each row can use a
different account. Channel names can contain hyphens, so the value is not
split on every hyphen: each hyphen, left to right, is tried as the
account/channel boundary, keeping only splits whose channel part is a valid
Slack channel name, and the first split Datadog does not answer with 404 is
used. Values with no valid split are skipped.

The DD_APP_KEY user needs the "Integrations Manage" permission. Failures are
counted in the returned summary and never fail the monitor run.
"""

import json
import re
import time
from urllib.parse import quote

import requests

from monitors import dd_client

MAX_RETRIES = 5
BACKOFF_SECONDS = 2
TIMEOUT_SECONDS = 30

# Slack channel names: lowercase letters, digits, hyphens, underscores; max 80.
_SLACK_CHANNEL_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,79}$")

# Status codes that mean "channel not usable here": warn and skip.
_SKIP_ERRORS = {
    403: "the DD_APP_KEY user needs the 'Integrations Manage' "
         "(integrations_manage) permission.",
    404: "account or channel is not set up in the Datadog Slack integration.",
}


class SlackDisplayError(Exception):
    """Per-channel failure. *kind* is "skipped" (setup issue) or "failed"."""

    def __init__(self, message, kind="failed", status=None):
        super().__init__(message)
        self.kind = kind
        self.status = status


def _split_candidates(value):
    """
    Possible (account, "#channel") splits of a Slack_Channel value, trying
    each hyphen left to right. Only splits with a non-empty account (no
    whitespace) and a valid Slack channel name are returned.
    """
    candidates = []
    for i, char in enumerate(value):
        if char != "-":
            continue
        account, channel = value[:i], value[i + 1:].lstrip("#")
        if account and not re.search(r"\s", account) and _SLACK_CHANNEL_RE.match(channel):
            candidates.append((account, "#" + channel))
    return candidates


def _channel_url(account, channel):
    return "{}/api/v1/integration/slack/configuration/accounts/{}/channels/{}".format(
        dd_client.dd_api_base(), quote(account, safe=""), quote(channel, safe="")
    )


def _request(method, url, body=None):
    """Send a request, retrying 429 and 5xx with exponential backoff."""
    delay = BACKOFF_SECONDS
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = requests.request(
                method,
                url,
                headers=dd_client.headers(),
                data=json.dumps(body) if body is not None else None,
                timeout=TIMEOUT_SECONDS,
            )
        except requests.exceptions.RequestException as e:
            raise SlackDisplayError("network error: {}".format(e))

        code = response.status_code
        if code < 300:
            return response.json() if response.content else {}

        if (code == 429 or code >= 500) and attempt < MAX_RETRIES:
            reset = response.headers.get("X-RateLimit-Reset", "")
            wait = max(int(reset), 1) if code == 429 and reset.isdigit() else delay
            time.sleep(wait)
            delay *= 2
            continue

        detail = (response.text or "").strip()[:200]
        if code in _SKIP_ERRORS:
            raise SlackDisplayError(
                "HTTP {}: {} {}".format(code, _SKIP_ERRORS[code], detail),
                kind="skipped", status=code)
        if code == 401:
            raise SlackDisplayError(
                "HTTP 401: DD_API_KEY / DD_APP_KEY rejected (or wrong DD_SITE). " + detail,
                status=code)
        raise SlackDisplayError("HTTP {}: {}".format(code, detail), status=code)

    raise SlackDisplayError("gave up after {} retries".format(MAX_RETRIES))


def _ensure_channel(account, channel):
    """Returns "updated" or "already_correct"."""
    url = _channel_url(account, channel)
    current = _request("GET", url)
    display = current.get("display") or {}
    if display.get("tags") is False:
        return "already_correct"

    _request("PATCH", url, {
        "name": current.get("name") or channel,
        "display": dict(display, tags=False),
    })
    return "updated"


def ensure_slack_tags_hidden(slack_channels):
    """
    Turn off the Tags section on every channel in *slack_channels* (CSV
    Slack_Channel values). Never raises. Returns the summary dict of lists of
    CSV values.
    """
    summary = {"updated": [], "already_correct": [], "skipped": [], "failed": []}

    seen = set()
    for value in slack_channels:
        value = (value or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)

        candidates = _split_candidates(value)
        if not candidates:
            summary["skipped"].append(value)
            continue

        try:
            for i, (account, channel) in enumerate(candidates):
                try:
                    outcome = _ensure_channel(account, channel)
                    break
                except SlackDisplayError as e:
                    # 404 may just mean the wrong boundary; try the next split.
                    if e.status == 404 and i < len(candidates) - 1:
                        continue
                    raise
        except SlackDisplayError as e:
            outcome = e.kind
        except Exception:  # never fail the monitor run over this step
            outcome = "failed"
        summary[outcome].append(value)

    return summary
