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
        # Structured alarm message; named %(key)s substitution below (order-safe)
        "message": (
            "**State Change**\n"
            "{{#is_recovery}}ALARM → OK{{/is_recovery}}{{#is_alert}}OK → ALARM{{/is_alert}}\n"
            "\n"
            "**Region**\n"
            "%(location)s\n"
            "\n"
            "Description\n"
            "{{#is_alert}}CRITICAL: The SSL certificate for %(domain)s in %(tier)s tier is "
            "expiring within 30 days or is invalid. This indicates the certificate may need "
            "renewal, meaning the service could become inaccessible over HTTPS.{{/is_alert}}\n"
            "{{#is_recovery}}RESOLVED: The SSL certificate for %(domain)s in %(tier)s tier is "
            "valid and not expiring within 30 days.{{/is_recovery}}\n"
            "\n"
            "%(notification)s"
        ) % {
            "location": ", ".join(locations),
            "domain": domain,
            "tier": tier,
            "notification": notification,
        },
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
