#!/usr/bin/python
"""
Hide the "Tags" section in Datadog's Slack alerts.

Why: every Slack alert Datadog posts ends with a "Tags" section (e.g.
"check_type:browser, project:cbioportal, tier:dev"). That section is not part
of the monitor message, so neither the message template nor the
notification preset removes it. It comes from the Datadog Slack
integration's per-channel display setting "tags".

What: for each Slack channel our monitors notify, this module sets
display.tags = false and leaves every other display setting (message,
notified, snapshot, mute_buttons) exactly as it is. It does not touch the
monitors, their messages or their project:/tier: tags.

Datadog API v1, Slack Integration:
  GET   /api/v1/integration/slack/configuration/accounts/{account_name}/channels/{channel_name}
  PATCH /api/v1/integration/slack/configuration/accounts/{account_name}/channels/{channel_name}
        body: {"name": "#channel", "display": {..current values.., "tags": false}}

Channel names: the CSV's Slack_Channel column holds the part after
"@slack-" in the notification handle, i.e. "<account>-<channel>", e.g.
"Expand_Data_Commons-ccdi-subprod-cbio" -> account "Expand_Data_Commons",
channel "#ccdi-subprod-cbio". The account name is NOT guessed from the value:
it comes from DD_SLACK_ACCOUNT_NAME (default "Expand_Data_Commons"), and only
values that start with "<account>-" are processed. Anything else is reported
as skipped.

Permissions: the DD_APP_KEY user needs the "Integrations Manage" permission
(integrations_manage). Without it Datadog returns 403. This step logs a
warning and the monitor run still succeeds.

Auth and site: same as the rest of the scripts (dd_client.headers() and
dd_client.dd_api_base(), i.e. DD_API_KEY / DD_APP_KEY / DD_SITE from the
environment). Key values are never printed.

Run locally (dry run makes no changes in Datadog):
    export DD_API_KEY=... DD_APP_KEY=... DD_SITE=ddog-gov.com
    python3 monitoring/scripts/datadog/monitor_update_csv.py -f <csv URL> --dry-run
"""

import json
import os
import time
from urllib.parse import quote

import requests

from monitors import dd_client

DEFAULT_SLACK_ACCOUNT = "Expand_Data_Commons"

# 429 / 5xx retries: waits 2, 4, 8, 16, 32 s (or X-RateLimit-Reset on 429).
MAX_RETRIES = 5
BACKOFF_SECONDS = 2
TIMEOUT_SECONDS = 30


class SlackDisplayError(Exception):
    """Per-channel failure. *kind* is "skipped" (setup issue) or "failed"."""

    def __init__(self, message, kind="failed"):
        super().__init__(message)
        self.kind = kind


def slack_account_name():
    return (os.getenv("DD_SLACK_ACCOUNT_NAME") or DEFAULT_SLACK_ACCOUNT).strip()


def _channel_url(account, channel):
    return "{}/api/v1/integration/slack/configuration/accounts/{}/channels/{}".format(
        dd_client.dd_api_base(), quote(account, safe=""), quote(channel, safe="")
    )


def _request(method, url, body=None):
    """
    Send one request with dd_client's headers, retrying 429 and 5xx with
    exponential backoff. Returns the parsed JSON body; raises
    SlackDisplayError with an operator-friendly message otherwise.
    """
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
            wait = delay
            reset = response.headers.get("X-RateLimit-Reset", "")
            if code == 429 and reset.isdigit():
                wait = max(int(reset), 1)
            print("    HTTP {} on {}, retrying in {}s ({}/{}).".format(
                code, method, wait, attempt + 1, MAX_RETRIES))
            time.sleep(wait)
            delay *= 2
            continue

        detail = (response.text or "").strip()[:200]
        if code == 401:
            raise SlackDisplayError(
                "HTTP 401: DD_API_KEY / DD_APP_KEY rejected (or wrong DD_SITE). " + detail)
        if code == 403:
            raise SlackDisplayError(
                "HTTP 403: the DD_APP_KEY user needs the 'Integrations Manage' "
                "(integrations_manage) permission. " + detail, kind="skipped")
        if code == 404:
            raise SlackDisplayError(
                "HTTP 404: account or channel is not set up in the Datadog Slack "
                "integration (Datadog -> Integrations -> Slack). " + detail, kind="skipped")
        raise SlackDisplayError("HTTP {}: {}".format(code, detail))

    raise SlackDisplayError("gave up after {} retries".format(MAX_RETRIES))


def _ensure_channel(account, channel, dry_run):
    """Returns "updated", "would_update" or "already_correct"."""
    url = _channel_url(account, channel)

    current = _request("GET", url)
    display = dict(current.get("display") or {})
    if display.get("tags") is False:
        return "already_correct"

    new_display = dict(display, tags=False)
    print("  {}: display {} -> {}".format(
        channel, json.dumps(display, sort_keys=True), json.dumps(new_display, sort_keys=True)))
    if dry_run:
        return "would_update"

    _request("PATCH", url, {"name": current.get("name") or channel, "display": new_display})
    return "updated"


def ensure_slack_tags_hidden(slack_channels, dry_run=False):
    """
    Turn off the Tags section on every Slack channel in *slack_channels*
    (CSV Slack_Channel values, "<account>-<channel>"). Never raises: every
    problem is logged and counted so the monitor run is not failed by it.
    Returns the summary dict of channel lists.
    """
    account = slack_account_name()
    prefix = account + "-"
    summary = {"updated": [], "would_update": [], "already_correct": [],
               "skipped": [], "failed": []}

    print()
    print("Slack channel display: hiding Tags (account {}){}".format(
        account, " [DRY RUN]" if dry_run else ""))
    print()

    seen = set()
    for value in slack_channels:
        value = (value or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)

        if not value.startswith(prefix):
            print("  {}: skipped, does not start with '{}' (check the CSV "
                  "Slack_Channel value or DD_SLACK_ACCOUNT_NAME).".format(value, prefix))
            summary["skipped"].append(value)
            continue

        channel = "#" + value[len(prefix):].lstrip("#")
        try:
            outcome = _ensure_channel(account, channel, dry_run)
        except SlackDisplayError as e:
            label = "WARNING" if e.kind == "skipped" else "ERROR"
            print("  {}: {} {}".format(channel, label, e))
            summary[e.kind].append(channel)
            continue
        except Exception as e:  # never fail the monitor run over this step
            print("  {}: ERROR unexpected {}: {}".format(channel, type(e).__name__, e))
            summary["failed"].append(channel)
            continue

        print("  {}: {}".format(channel, outcome.replace("_", " ")))
        summary[outcome].append(channel)

    print()
    print("Slack channel display summary: {} {}, {} already correct, "
          "{} skipped, {} failed.".format(
              len(summary["would_update"]) if dry_run else len(summary["updated"]),
              "would update" if dry_run else "updated",
              len(summary["already_correct"]),
              len(summary["skipped"]),
              len(summary["failed"])))
    return summary
