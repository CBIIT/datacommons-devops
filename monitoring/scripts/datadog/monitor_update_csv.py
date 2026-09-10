#!/usr/bin/python
"""
DataDog monitoring automation — CSV-driven entrypoint.

Reads the same FNL-Monitoring-List.csv used by the New Relic scripts and
provisions the equivalent DataDog resources:
  - Synthetic tests (API HTTP, multi-step API, browser, SSL)
  - Metric alert monitors (ALB, ECS Fargate, OpenSearch)

Required environment variables:
  DD_API_KEY              DataDog API key
  DD_APP_KEY              DataDog application key
  DD_ALERT_EMAIL          Fallback alert email (used when CSV Alert_Email is blank)
  DD_PRIVATE_LOCATION_ID  Private synthetics location ID (e.g. pl:name:abc123)
  DD_SITE                 Optional — DataDog site, defaults to datadoghq.com

DataDog Slack notifications use @slack-<workspace>-<channel> syntax. The
Slack_Channel values in the CSV are channel IDs; these must match a channel
name configured in the DataDog Slack integration. Update the slack_channel
handling in _make_notification() if your workspace uses a different scheme.

New CSV columns (all optional — leave Downtime_Start blank to skip):
  Downtime_Start   "HH:MM" 24-hour local start time, e.g. "19:00"
  Downtime_End     "HH:MM" 24-hour local end time, e.g. "07:00"
  Downtime_TZ      IANA timezone, e.g. "America/New_York"
  Downtime_Days    optional comma list of weekdays, e.g. "MO,TU,WE,TH,FR"
                    (blank = every day)

Usage:
    python3 monitor_update_csv.py -f <CSV_URL>
"""

import sys
import getopt
import json
import os
import csv
import codecs
import contextlib
import datetime

import requests

from monitors.synthetics import (
    set_api_http_monitor,
    set_api_multistep_monitor,
    set_browser_monitor,
    set_ssl_monitor,
)
from monitors.alerts.fargate import (
    set_fargate_cpu_monitor,
    set_fargate_mem_monitor,
    set_fargate_restarts_monitor,
)
from monitors.alerts.alb import (
    set_alb_4xx_monitor,
    set_alb_5xx_monitor,
    set_alb_target_5xx_monitor,
    set_alb_response_time_monitor,
    set_alb_tls_monitor,
    set_alb_unhealthy_hosts_monitor,
)
from monitors.alerts.opensearch import set_os_cluster_red_monitor
from monitors.downtime import set_recurring_downtime


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hf:", ["file="])
    except getopt.GetoptError:
        print("File URL required:   monitor_update_csv.py -f <file>")
        sys.exit(2)

    input_url = None
    for opt, arg in opts:
        if opt == "-h":
            print("monitor_update_csv.py -f <file>")
            sys.exit()
        elif opt in ("-f", "--file"):
            input_url = arg

    if not input_url:
        print("File URL required:   monitor_update_csv.py -f <file>")
        sys.exit(2)

    setMonitors(input_url)
    setSynthetics(input_url)


def _make_notification(alert_email, slack_channel):
    """Build the @-mention notification string embedded in every DD monitor message."""
    parts = []
    if alert_email:
        parts.append("@email:{}".format(alert_email))
    # DataDog Slack: @slack-<workspace>-<channel-name>
    # The CSV stores channel IDs; update accordingly once your DD Slack
    # integration is configured with matching channel names.
    if slack_channel:
        parts.append("@slack-{}".format(slack_channel))
    return " ".join(parts)

def _maybe_set_downtime(row, monitor_id, label):
    """
    Reads Downtime_Start / Downtime_End / Downtime_TZ / Downtime_Days from
    the CSV row and, if present, schedules/updates a recurring downtime for
    the given monitor_id. No-ops silently if Downtime_Start is blank.
    """
    downtime_start = (row.get("Downtime_Start") or "").strip()
    if not downtime_start:
        return

    if not monitor_id:
        print(
            "  Skipping downtime for {} — monitor was not created "
            "(or its ID wasn't returned) this run.".format(label)
        )
        return

    downtime_end = (row.get("Downtime_End") or "").strip()
    downtime_tz = (row.get("Downtime_TZ") or "UTC").strip()
    days_raw = (row.get("Downtime_Days") or "").strip()
    days_of_week = [d.strip().upper() for d in days_raw.split(",")] if days_raw else None

    if not downtime_end:
        print(
            "  Skipping downtime for {} — Downtime_Start given but "
            "Downtime_End is blank.".format(label)
        )
        return

    # First occurrence date: today, in whatever local date the box running
    # this script considers "today". Since the schedule recurs daily (or on
    # specific weekdays) indefinitely, the exact first date mostly just
    # needs to be "on or before now" — Datadog will roll forward to the
    # next valid occurrence per the rrule.
    start_date = datetime.date.today().isoformat()

    print(
        "  Scheduling downtime for {}: {}-{} {} (days={})".format(
            label, downtime_start, downtime_end, downtime_tz, days_of_week or "daily"
        )
    )

    set_recurring_downtime.setdowntime(
        monitor_id=monitor_id,
        downtime_start=downtime_start,
        downtime_end=downtime_end,
        timezone=downtime_tz,
        message="Auto-scheduled: service shut down for cost savings during this window.",
        days_of_week=days_of_week,
        start_date=start_date,
    )

def setMonitors(input_url):
    """Provision infrastructure metric-alert monitors (ALB, Fargate, OpenSearch)."""
    with contextlib.closing(requests.get(input_url, stream=True)) as csvfile:
        data = csv.DictReader(codecs.iterdecode(csvfile.iter_lines(), "utf-8"))
        tiers_set = []

        for row in data:
            project = row["Project_Acronym"].upper()
            tier = row["Tier"]
            alert_email = row["Alert_Email"] or os.getenv("DD_ALERT_EMAIL", "")
            slack_channel = row["Slack_Channel"]
            resources = [r.strip() for r in row["Monitored_Resources"].split(",")]
            notification = _make_notification(alert_email, slack_channel)

            if project + "-" + tier not in tiers_set:
                print()
                print("Adding Monitor Configuration For: {} {}".format(project, tier))
                print()

                if "opensearch" in resources:
                    print("adding opensearch config")
                    monitor_id = set_os_cluster_red_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(row, monitor_id, "{} {} opensearch".format(project, tier))

                if "alb" in resources:
                    print("adding alb config")
                    monitor_id = set_alb_4xx_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(row, monitor_id, "{} {} alb-4xx".format(project, tier))

                    monitor_id = set_alb_5xx_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(row, monitor_id, "{} {} alb-5xx".format(project, tier))

                    monitor_id = set_alb_target_5xx_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(
                        row, monitor_id, "{} {} alb-target-5xx".format(project, tier)
                    )

                    monitor_id = set_alb_response_time_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(
                        row, monitor_id, "{} {} alb-response-time".format(project, tier)
                    )

                    monitor_id = set_alb_tls_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(row, monitor_id, "{} {} alb-tls".format(project, tier))

                    monitor_id = set_alb_unhealthy_hosts_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(
                        row, monitor_id, "{} {} alb-unhealthy-hosts".format(project, tier)
                    )

                if "fargate" in resources:
                    print("adding fargate config")
                    monitor_id = set_fargate_cpu_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(
                        row, monitor_id, "{} {} fargate-cpu".format(project, tier)
                    )

                    monitor_id = set_fargate_mem_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(
                        row, monitor_id, "{} {} fargate-mem".format(project, tier)
                    )

                    monitor_id = set_fargate_restarts_monitor.setmonitor(project, tier, notification)
                    _maybe_set_downtime(
                        row, monitor_id, "{} {} fargate-restarts".format(project, tier)
                    )

                tiers_set.append(project + "-" + tier)


def setSynthetics(input_url):
    """Provision DataDog Synthetic tests for each endpoint row in the CSV."""
    with contextlib.closing(requests.get(input_url, stream=True)) as csvfile:
        data = csv.DictReader(codecs.iterdecode(csvfile.iter_lines(), "utf-8"))

        for row in data:
            project = row["Project_Acronym"].upper()
            tier = row["Tier"]
            endpoint_name = row["Endpoint_Name"]
            monitor_url = row["URL"]
            alert_email = row["Alert_Email"] or os.getenv("DD_ALERT_EMAIL", "")
            slack_channel = row["Slack_Channel"]
            notification = _make_notification(alert_email, slack_channel)
            label = "{} {} {}".format(project, tier, endpoint_name)

            print()
            print("Adding Synthetics Configuration For: {}".format(label))
            print()

            api = {
                "name": endpoint_name,
                "url": monitor_url,
                "location": row["Private_Location"],
                "query": row["Endpoint_Query"],
                "browser_query": row["Browser_Query"],
                "text": row["Validation_Text"],
            }

            monitor_id = None

            if api["query"]:
                # NR Scripted API → DD multi-step API test
                monitor_id = set_api_multistep_monitor.setmonitor(project, tier, api, notification)
            elif api["browser_query"] or api["text"]:
                # NR Scripted Browser, or Validation_Text with no script at
                # all (assume the page may be JS-rendered, so a raw HTTP
                # body-contains check can't be trusted) → DD browser test
                monitor_id = set_browser_monitor.setmonitor(project, tier, api, notification)
                if tier.lower() == "prod" and api["name"].lower() == "portal":
                    ssl_id = set_ssl_monitor.setmonitor(project, tier, api, notification)
                    _maybe_set_downtime(row, ssl_id, label + " ssl")
            elif tier.lower() == "prod" and api["name"].lower() == "portal":
                # Prod portal with no script/validation text: HTTP check + SSL certificate check
                monitor_id = set_api_http_monitor.setmonitor(project, tier, api, notification)
                ssl_id = set_ssl_monitor.setmonitor(project, tier, api, notification)
                _maybe_set_downtime(row, ssl_id, label + " ssl")
            else:
                # All other endpoints: simple HTTP availability check
                monitor_id = set_api_http_monitor.setmonitor(project, tier, api, notification)
            _maybe_set_downtime(row, monitor_id, label)


if __name__ == "__main__":
    main(sys.argv[1:])
