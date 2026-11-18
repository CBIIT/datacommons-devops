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
    monitor_name = dd_client.synthetic_test_name(project, tier, api["name"])
    freq = dd_client.tick_every(tier, project)
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
            **dd_client.failure_options(project, tier),
        },
        "status": "live",
        "tags": dd_client.synthetic_tags(project, tier, api["name"]),
        "type": "api",
        "subtype": "http",
    }

    return dd_client.upsert_and_report(monitor_name, "api", payload)
