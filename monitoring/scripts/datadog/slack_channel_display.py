#!/usr/bin/python
"""
Hide the "Tags" and "Notified" sections in Datadog's Slack alerts.

Those two sections are not part of a monitor's message. The Datadog Slack
integration adds them, and they are switched on or off per Slack channel.
This script turns both off for every Slack channel used in the monitoring
CSV and leaves the channel's other display settings (message, snapshot,
mute buttons) as they are.

It does not remove the "Triggered: [Synthetics] <monitor name>" title. The
Slack integration always adds that title, and only a Datadog Webhook ->
Slack Incoming Webhook route can drop it.

The CSV's Slack_Channel values are "<account>-<channel>", the same string
used in the @slack-<account>-<channel> handle, e.g.
"Expand_Data_Commons-crdc-prod-cds" -> account "Expand_Data_Commons",
channel "#crdc-prod-cds". Values that do not start with "<account>-" are
reported and skipped.

Required environment variables:
  DD_API_KEY   DataDog API key
  DD_APP_KEY   DataDog application key (needs the manage_integrations permission)
  DD_SITE      Optional, defaults to datadoghq.com (use ddog-gov.com for gov)

Usage:
    # Dry run (default): show what would change, make no changes
    python3 slack_channel_display.py -f <CSV path or URL>

    # Apply the changes
    python3 slack_channel_display.py -f <CSV path or URL> --apply

    # Different Slack integration account name
    python3 slack_channel_display.py -f <CSV> --account <name>
"""

import argparse
import codecs
import contextlib
import csv
import json
import sys
from urllib.parse import quote

import requests

from monitors import dd_client

DEFAULT_ACCOUNT = "Expand_Data_Commons"
HIDE = {"tags": False, "notified": False}


def read_slack_values(source):
    """Return the distinct, non-blank Slack_Channel values from the CSV."""
    if source.startswith(("http://", "https://")):
        with contextlib.closing(requests.get(source, stream=True)) as resp:
            resp.raise_for_status()
            rows = list(csv.DictReader(codecs.iterdecode(resp.iter_lines(), "utf-8")))
    else:
        with open(source, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
    return sorted({(r.get("Slack_Channel") or "").strip() for r in rows} - {""})


def channel_url(account, channel):
    return "{}/api/v1/integration/slack/configuration/accounts/{}/channels/{}".format(
        dd_client.dd_api_base(), quote(account, safe=""), quote(channel, safe="")
    )


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("-f", "--file", required=True, help="CSV path or URL")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT,
                        help="Datadog Slack integration account name")
    parser.add_argument("--apply", action="store_true",
                        help="Make the changes (default is a dry run)")
    args = parser.parse_args(argv)

    prefix = args.account + "-"
    h = dd_client.headers()
    failures = 0

    for value in read_slack_values(args.file):
        if not value.startswith(prefix):
            print("SKIP   {!r}: does not start with {!r}; check the CSV.".format(value, prefix))
            failures += 1
            continue

        channel = "#" + value[len(prefix):]
        url = channel_url(args.account, channel)

        resp = requests.get(url, headers=h)
        if resp.status_code == 404:
            print("MISSING {}: not configured in the Slack integration.".format(channel))
            failures += 1
            continue
        try:
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("ERROR  {}: {}".format(channel, e))
            failures += 1
            continue

        display = dict(resp.json().get("display") or {})
        if all(display.get(k) is v for k, v in HIDE.items()):
            print("OK     {}: tags and notified already hidden.".format(channel))
            continue

        new_display = dict(display, **HIDE)
        if not args.apply:
            print("WOULD  {}: {} -> {}".format(channel, display, new_display))
            continue

        try:
            requests.patch(
                url, headers=h,
                data=json.dumps({"name": channel, "display": new_display}),
            ).raise_for_status()
        except requests.exceptions.RequestException as e:
            print("ERROR  {}: {}".format(channel, e))
            failures += 1
            continue
        print("UPDATED {}: tags and notified hidden.".format(channel))

    if not args.apply:
        print("\nDry run only. Re-run with --apply to make these changes.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
