#!/usr/bin/python
"""
DataDog SSL certificate synthetic test.

Replaces: New Relic Cert Check monitor (syntheticsCreateCertCheckMonitor)

DataDog equivalent: API test, subtype 'ssl'
  - Checks that the SSL certificate on the target host does not expire within
    30 days (same threshold as the New Relic monitor).
  - Runs once per day (same as New Relic EVERY_DAY period).
  - Created only for Prod Portal endpoints (caller decides when to invoke this).
"""

from monitors import dd_client


def setmonitor(project, tier, api, notification):
    monitor_name = "{} {} Certificate Monitor".format(project, tier)
    # Strip scheme and trailing slashes to get bare hostname
    domain = api["url"].replace("https://", "").replace("http://", "").rstrip("/")
    freq = 86400  # once per day in seconds

    locations = dd_client.synthetics_location(api["location"])

    payload = {
        "config": {
            "assertions": [
                # Fail if certificate expires in fewer than 30 days
                {"operator": "isInMoreThan", "type": "certificate", "target": 30},
            ],
            "request": {
                "host": domain,
                "port": 443,
            },
        },
        "locations": locations,
        "message": "{} {} SSL certificate is expiring soon or invalid.\n{}".format(
            project, tier, notification
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
        "subtype": "ssl",
    }

    public_id = dd_client.find_synthetic_test(monitor_name)
    if public_id:
        print("{} already exists, updating with latest configuration.".format(monitor_name))
    else:
        print("{} not found, creating.".format(monitor_name))

    public_id = dd_client.upsert_synthetic_test(public_id, "api", payload)
    print("{} upserted (public_id: {}).".format(monitor_name, public_id))
    return public_id
