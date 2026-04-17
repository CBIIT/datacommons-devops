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
    freq = 600 if tier.lower() == "prod" else 1800  # seconds
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
        "message": "{} {} {} is down or unreachable.\n{}".format(
            project, tier, api["name"], notification
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
            "ssl_certificate": True,
        },
        "status": "live",
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "type": "api",
        "subtype": "http",
    }

    public_id = dd_client.find_synthetic_test(monitor_name)
    if public_id:
        print("{} already exists, updating with latest configuration.".format(monitor_name))
    else:
        print("{} not found, creating.".format(monitor_name))

    public_id = dd_client.upsert_synthetic_test(public_id, "api", payload)
    print("{} upserted (public_id: {}).".format(monitor_name, public_id))
    return public_id
