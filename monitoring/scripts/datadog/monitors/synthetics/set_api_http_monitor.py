#!/usr/bin/python
"""
DataDog API HTTP synthetic test.

Replaces: New Relic Simple Browser monitor (syntheticsCreateSimpleBrowserMonitor)

DataDog equivalent: API test, subtype 'http'
  - Checks that the URL returns HTTP 200.
  - Optionally asserts that the response body contains a validation string.
  - Runs every 10 min (prod) or 30 min (other tiers).
  - Performs TLS validation automatically when the URL is HTTPS.
"""

from monitors import dd_client


def setmonitor(project, tier, api, notification):
    monitor_name = "{} {} {} Monitor".format(project, tier, api["name"])
    freq = dd_client.tick_every(tier)
    locations = dd_client.synthetics_location(api["location"])

    assertions = [
        {"operator": "is", "type": "statusCode", "target": 200},
    ]
    if api.get("text"):
        assertions.append(
            {"operator": "contains", "type": "body", "target": api["text"]}
        )

    payload = {
        "config": {
            "assertions": assertions,
            "request": {
                "method": "GET",
                "url": api["url"],
            },
        },
        "locations": locations,
        "message": dd_client.build_synthetic_alert_message(
            monitor_name, "GET {}".format(api["url"]), notification
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
            "monitor_options": dd_client.synthetic_monitor_options(),
        },
        "status": "live",
        "tags": dd_client.default_tags(project, tier),
        "type": "api",
        "subtype": "http",
    }

    return dd_client.upsert_and_report(monitor_name, "api", payload)
