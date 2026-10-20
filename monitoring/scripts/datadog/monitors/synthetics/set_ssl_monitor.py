#!/usr/bin/python
"""
DataDog SSL certificate synthetic test.

Replaces: New Relic Cert Check monitor (syntheticsCreateCertCheckMonitor)

DataDog equivalent: API test, subtype 'ssl'
  - Checks that the SSL certificate on the target host does not expire within
    30 days (same threshold as the New Relic monitor).
  - Runs once per day (same as New Relic EVERY_DAY period).
  - Retries transient failures before alerting, so a single network/handshake
    blip from the probing location does not page a false "cert invalid".
  - Created only for Prod Portal endpoints (caller decides when to invoke this).
"""

from monitors import dd_client


def setmonitor(project, tier, api, notification):
    monitor_name = "{} {} Certificate Monitor".format(project, tier)
    # Strip scheme and trailing slashes to get bare hostname
    domain = api["url"].replace("https://", "").replace("http://", "").rstrip("/")
    freq = 86400  # once per day in seconds

    locations = dd_client.synthetics_location(api["location"])
    description_fmt = {"domain": domain, "tier": tier}

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
        "message": dd_client.build_alarm_message(
            locations,
            (
                "CRITICAL: The SSL certificate for %(domain)s in %(tier)s tier is expiring "
                "within 30 days or is invalid. This indicates the certificate may need "
                "renewal, meaning the service could become inaccessible over HTTPS."
            ) % description_fmt,
            (
                "RESOLVED: The SSL certificate for %(domain)s in %(tier)s tier is valid and "
                "not expiring within 30 days."
            ) % description_fmt,
            notification,
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
            # Retry transient failures before alerting. This SSL check runs only
            # once per day from a single (often cross-partition) location, so
            # without retries a lone network/handshake blip fires a CRITICAL
            # "cert expiring/invalid" alert even when the certificate is valid.
            # Two quick retries smooth these false positives.
            "retry": {"count": 2, "interval": 5000},  # interval in ms
        },
        "status": "live",
        "tags": dd_client.default_tags(project, tier),
        "type": "api",
        "subtype": "ssl",
    }

    return dd_client.upsert_and_report(monitor_name, "api", payload)
