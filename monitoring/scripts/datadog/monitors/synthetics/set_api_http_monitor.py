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

    description_fmt = {"name": api["name"], "tier": tier, "url": api["url"]}

    payload = {
        "config": {
            "assertions": assertions,
            "request": {
                "method": "GET",
                "url": api["url"],
            },
        },
        "locations": locations,
        "message": dd_client.build_alarm_message(
            locations,
            (
                "CRITICAL: The %(name)s endpoint in %(tier)s tier is failing its synthetic "
                "HTTP availability check (GET %(url)s). This indicates the endpoint is "
                "returning an unexpected status code or failing response validation, meaning "
                "the service may be unavailable or misbehaving."
            ) % description_fmt,
            (
                "RESOLVED: The %(name)s endpoint in %(tier)s tier has recovered and is "
                "passing its synthetic HTTP availability check (GET %(url)s)."
            ) % description_fmt,
            notification,
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
        },
        "status": "live",
        "tags": dd_client.default_tags(project, tier),
        "type": "api",
        "subtype": "http",
    }

    return dd_client.upsert_and_report(monitor_name, "api", payload)
