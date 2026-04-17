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
                    set_os_cluster_red_monitor.setmonitor(project, tier, notification)

                if "alb" in resources:
                    print("adding alb config")
                    set_alb_4xx_monitor.setmonitor(project, tier, notification)
                    set_alb_5xx_monitor.setmonitor(project, tier, notification)
                    set_alb_target_5xx_monitor.setmonitor(project, tier, notification)
                    set_alb_response_time_monitor.setmonitor(project, tier, notification)
                    set_alb_tls_monitor.setmonitor(project, tier, notification)
                    set_alb_unhealthy_hosts_monitor.setmonitor(project, tier, notification)

                if "fargate" in resources:
                    print("adding fargate config")
                    set_fargate_cpu_monitor.setmonitor(project, tier, notification)
                    set_fargate_mem_monitor.setmonitor(project, tier, notification)
                    set_fargate_restarts_monitor.setmonitor(project, tier, notification)

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

            print()
            print(
                "Adding Synthetics Configuration For: {} {} {}".format(
                    project, tier, endpoint_name
                )
            )
            print()

            api = {
                "name": endpoint_name,
                "url": monitor_url,
                "location": row["Private_Location"],
                "query": row["Endpoint_Query"],
                "browser_query": row["Browser_Query"],
                "text": row["Validation_Text"],
            }

            if api["query"]:
                # NR Scripted API → DD multi-step API test
                set_api_multistep_monitor.setmonitor(project, tier, api, notification)
            elif api["browser_query"]:
                # NR Scripted Browser → DD browser test
                set_browser_monitor.setmonitor(project, tier, api, notification)
            elif tier.lower() == "prod" and api["name"].lower() == "portal":
                # Prod portal: HTTP check + SSL certificate check
                set_api_http_monitor.setmonitor(project, tier, api, notification)
                set_ssl_monitor.setmonitor(project, tier, api, notification)
            else:
                # All other endpoints: simple HTTP availability check
                set_api_http_monitor.setmonitor(project, tier, api, notification)


if __name__ == "__main__":
    main(sys.argv[1:])
