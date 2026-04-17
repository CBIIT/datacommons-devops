#!/usr/bin/python
"""
DataDog multi-step API synthetic test.

Replaces: New Relic Scripted API monitor (syntheticsCreateScriptApiMonitor,
          Node 16.10 runtime using $http.post).

DataDog equivalent: API test, subtype 'multi' (multi-step API test)
  - Each step is an HTTP request with assertions evaluated server-side.
  - The original New Relic monitor contains an inline Node.js script in the
    CSV Endpoint_Query column. DataDog does not execute arbitrary Node.js;
    the script must be converted to a sequence of HTTP steps using DataDog's
    step schema (method, URL, headers, body, assertions).
  - This module creates a single-step POST to the monitored URL as a starting
    point. Review and expand the 'steps' list to fully replicate your original
    New Relic script logic.

Runs every 10 min (prod) or 30 min (other tiers).
"""

from monitors import dd_client


def setmonitor(project, tier, api, notification):
    monitor_name = "{} {} {} Monitor".format(project, tier, api["name"])
    freq = 600 if tier.lower() == "prod" else 1800  # seconds
    locations = dd_client.synthetics_location(api["location"])

    # --------------------------------------------------------------------------
    # NOTE: The New Relic script (api['query']) is inline Node.js code that
    # cannot be automatically converted. The step below performs a basic HTTP
    # POST to the endpoint URL. Replace or extend 'steps' with the request
    # body, headers, and assertions that match your original script.
    # --------------------------------------------------------------------------
    payload = {
        "config": {
            "steps": [
                {
                    "name": "API check",
                    "subtype": "http",
                    "request": {
                        "method": "POST",
                        "url": api["url"],
                        "headers": {"Content-Type": "application/json"},
                        "body": "",  # populate with your request body
                    },
                    "assertions": [
                        {"operator": "is", "type": "statusCode", "target": 200},
                    ],
                }
            ]
        },
        "locations": locations,
        "message": "{} {} {} API check failed.\n{}".format(
            project, tier, api["name"], notification
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
        },
        "status": "live",
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "type": "api",
        "subtype": "multi",
    }

    public_id = dd_client.find_synthetic_test(monitor_name)
    if public_id:
        print("{} already exists, updating with latest configuration.".format(monitor_name))
    else:
        print("{} not found, creating.".format(monitor_name))

    public_id = dd_client.upsert_synthetic_test(public_id, "api", payload)
    print("{} upserted (public_id: {}).".format(monitor_name, public_id))
    return public_id
