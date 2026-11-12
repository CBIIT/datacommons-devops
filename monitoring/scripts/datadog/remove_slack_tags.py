#!/usr/bin/env python3
"""
Remove the "Tags" section from Datadog alerts posted to Slack.

The Tags section (e.g. "check_type:browser, project:cbioportal, tier:dev")
is added by the Datadog Slack integration's per-channel display settings; it
is not part of the monitor message. This script turns it off by setting
display.tags = false on each listed Slack channel.

What it changes:  ONLY the Slack integration channel's display.tags.
What it keeps:    every other display setting (message, notified, snapshot,
                  mute_buttons), exactly as currently configured.
What it never touches: the monitors or their tags (used for filtering and
                  routing).

Datadog API v1, Slack Integration:
  GET   /api/v1/integration/slack/configuration/accounts/{account_name}/channels/{channel_name}
  PATCH /api/v1/integration/slack/configuration/accounts/{account_name}/channels/{channel_name}
        body: {"name": "#channel", "display": {"message": .., "notified": ..,
               "snapshot": .., "tags": false, "mute_buttons": ..}}

Environment:
  DD_API_KEY          Datadog API key (required)
  DD_APP_KEY          Datadog application key (required). Its user needs the
                      "Integrations Manage" permission (integrations_manage).
  DD_SITE             Datadog site, default ddog-gov.com -> https://api.ddog-gov.com
  SLACK_ACCOUNT_NAME  Default for --account

Usage:
  python3 remove_slack_tags.py --account Expand_Data_Commons --channels channels.txt --dry-run
  python3 remove_slack_tags.py --account Expand_Data_Commons --channels channels.txt
  python3 remove_slack_tags.py --account Expand_Data_Commons --channel ccdi-subprod-cbio

Exit code: 0 if every channel ended with tags = false (or would, in a dry
run), 1 if any channel failed, 2 for bad arguments or missing keys.
"""

import argparse
import json
import os
import sys
import time
from urllib.parse import quote

import requests

# Retries for 429 (rate limited) and transient 5xx responses.
MAX_RETRIES = 5
BACKOFF_SECONDS = 2  # doubles on each retry: 2, 4, 8, 16, 32
TIMEOUT_SECONDS = 30


class ChannelError(Exception):
    """A per-channel failure with a message meant for the operator."""


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------

def load_channels(args):
    """
    Collect channel names from --channel (repeatable) and --channels <file>.
    The file has one channel per line; blank lines and lines starting with
    "#" followed by a space (comments) are ignored. Duplicates are removed,
    order is kept.
    """
    names = list(args.channel or [])
    if args.channels:
        with open(args.channels, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("# "):
                    continue
                names.append(line)
    seen, result = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            result.append(n)
    return result


def normalize_channel(raw, account):
    """
    Turn any of these into Datadog's stored channel name "#ccdi-subprod-cbio":
        ccdi-subprod-cbio
        #ccdi-subprod-cbio
        Expand_Data_Commons-ccdi-subprod-cbio   (the @slack-<account>-<channel>
                                                 form used in monitor messages)
    """
    name = raw.strip()
    if name.startswith("@slack-"):
        name = name[len("@slack-"):]
    if name.startswith(account + "-"):
        name = name[len(account) + 1:]
    return "#" + name.lstrip("#")


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

def api_request(session, method, url, body=None):
    """
    Send a request, retrying 429 and 5xx with exponential backoff.
    Raises ChannelError with an operator-friendly message on failure.
    Returns the parsed JSON body.
    """
    delay = BACKOFF_SECONDS
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = session.request(
                method, url,
                data=json.dumps(body) if body is not None else None,
                timeout=TIMEOUT_SECONDS,
            )
        except requests.exceptions.RequestException as e:
            raise ChannelError("network error: {}".format(e))

        code = resp.status_code
        if code < 300:
            return resp.json() if resp.content else {}

        retryable = code == 429 or code >= 500
        if retryable and attempt < MAX_RETRIES:
            # Datadog sends X-RateLimit-Reset (seconds) on 429; prefer it.
            wait = delay
            reset = resp.headers.get("X-RateLimit-Reset")
            if code == 429 and reset and reset.isdigit():
                wait = max(int(reset), 1)
            print("    {} {} -> HTTP {}, retrying in {}s ({}/{})".format(
                method, url, code, wait, attempt + 1, MAX_RETRIES))
            time.sleep(wait)
            delay *= 2
            continue

        raise ChannelError(explain_status(code, resp))

    raise ChannelError("gave up after {} retries".format(MAX_RETRIES))


def explain_status(code, resp):
    detail = (resp.text or "").strip()[:300]
    if code == 401:
        return ("HTTP 401 Unauthorized: DD_API_KEY or DD_APP_KEY is invalid, "
                "or belongs to a different Datadog site than DD_SITE. "
                + detail)
    if code == 403:
        return ("HTTP 403 Forbidden: the application key's user lacks the "
                "'Integrations Manage' (integrations_manage) permission, or "
                "the key is scoped without it. " + detail)
    if code == 404:
        return ("HTTP 404 Not Found: no such Slack account or channel in the "
                "Datadog Slack integration. Check --account (Datadog -> "
                "Integrations -> Slack) and the channel name. " + detail)
    if code == 429:
        return "HTTP 429 Too Many Requests: still rate limited after retries. " + detail
    return "HTTP {}: {}".format(code, detail)


# --------------------------------------------------------------------------
# Per-channel work
# --------------------------------------------------------------------------

def process_channel(session, base, account, channel, dry_run):
    """
    Returns "updated", "already_correct" or "would_update".
    Raises ChannelError on failure.
    """
    url = "{}/api/v1/integration/slack/configuration/accounts/{}/channels/{}".format(
        base, quote(account, safe=""), quote(channel, safe=""))

    # a. Current settings
    current = api_request(session, "GET", url)
    display = dict(current.get("display") or {})
    print("    current display: {}".format(json.dumps(display, sort_keys=True)))

    if display.get("tags") is False:
        return "already_correct"

    # b. Keep everything as-is, change only tags.
    new_display = dict(display, tags=False)
    print("    new display:     {}".format(json.dumps(new_display, sort_keys=True)))

    if dry_run:
        return "would_update"

    # c. Update
    api_request(session, "PATCH", url, {
        "name": current.get("name") or channel,
        "display": new_display,
    })

    # d. Verify
    after = (api_request(session, "GET", url).get("display") or {})
    if after.get("tags") is not False:
        raise ChannelError("update sent, but GET still shows tags = {!r}".format(after.get("tags")))
    changed = sorted(k for k in display if k != "tags" and after.get(k) != display.get(k))
    if changed:
        # Should not happen; surface it rather than silently accept it.
        raise ChannelError("tags is now false, but these settings also changed: {}".format(changed))
    print("    verified:        tags = false")
    return "updated"


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main(argv):
    parser = argparse.ArgumentParser(
        description="Turn off the 'Tags' section on Datadog Slack integration channels.")
    parser.add_argument("--account", default=os.getenv("SLACK_ACCOUNT_NAME"),
                        help="Slack account (workspace) name as configured in "
                             "Datadog. Default: $SLACK_ACCOUNT_NAME")
    parser.add_argument("--channels", metavar="FILE",
                        help="Text file with one channel name per line")
    parser.add_argument("--channel", action="append", metavar="NAME",
                        help="Channel name; repeat for several")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without changing anything")
    args = parser.parse_args(argv)

    if not args.account:
        parser.error("--account (or SLACK_ACCOUNT_NAME) is required")
    if not (args.channels or args.channel):
        parser.error("give --channels FILE and/or --channel NAME")

    api_key, app_key = os.getenv("DD_API_KEY"), os.getenv("DD_APP_KEY")
    if not api_key or not app_key:
        print("ERROR: set DD_API_KEY and DD_APP_KEY in the environment.", file=sys.stderr)
        return 2

    site = os.getenv("DD_SITE", "ddog-gov.com")
    base = "https://api.{}".format(site)

    try:
        raw_channels = load_channels(args)
    except OSError as e:
        print("ERROR: cannot read channel file: {}".format(e), file=sys.stderr)
        return 2
    channels = []
    for raw in raw_channels:
        c = normalize_channel(raw, args.account)
        if c not in channels:
            channels.append(c)

    session = requests.Session()
    session.headers.update({
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    })

    print("Datadog API: {}   Slack account: {}   Channels: {}{}".format(
        base, args.account, len(channels), "   (DRY RUN)" if args.dry_run else ""))

    results = {"updated": [], "would_update": [], "already_correct": [], "failed": []}
    for channel in channels:
        print("\n{}".format(channel))
        try:
            outcome = process_channel(session, base, args.account, channel, args.dry_run)
            results[outcome].append(channel)
            print("    -> {}".format(outcome.replace("_", " ")))
        except ChannelError as e:
            results["failed"].append(channel)
            print("    -> FAILED: {}".format(e))

    print("\nSummary")
    if args.dry_run:
        print("  would update:    {}".format(len(results["would_update"])))
    else:
        print("  updated:         {}".format(len(results["updated"])))
    print("  already correct: {}".format(len(results["already_correct"])))
    print("  failed:          {}".format(len(results["failed"])))
    for c in results["failed"]:
        print("    - {}".format(c))
    if args.dry_run:
        print("\nDry run: nothing was changed. Re-run without --dry-run to apply.")

    return 1 if results["failed"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
