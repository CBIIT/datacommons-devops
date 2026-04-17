#!/usr/bin/python
"""
DataDog Browser synthetic test.

Replaces: New Relic Scripted Browser monitor (syntheticsCreateScriptBrowserMonitor,
          Chrome 100 runtime).

DataDog equivalent: Browser test
  - DataDog browser tests use recorded steps stored as JSON (not free-form
    JavaScript), so the Chrome/WebDriver script in csv Browser_Query cannot
    be automatically converted.
  - This module creates a shell browser test targeting the monitored URL.
    Open the test in the DataDog UI (Synthetic Tests → edit) to record or
    import the equivalent steps from your original New Relic browser script.

Runs every 10 min (prod) or 30 min (other tiers).
"""

from monitors import dd_client


def setmonitor(project, tier, api, notification):
    monitor_name = "{} {} {} Monitor".format(project, tier, api["name"])
    freq = 600 if tier.lower() == "prod" else 1800  # seconds
    locations = dd_client.synthetics_location(api["location"])

    # --------------------------------------------------------------------------
    # NOTE: The New Relic scripted browser script (api['browser_query']) is
    # WebDriver-style JavaScript. DataDog browser tests use a different,
    # recorded-step format. The test is created here with the start URL only.
    # Use the DataDog UI to record the equivalent interaction steps.
    # --------------------------------------------------------------------------
    payload = {
        "config": {
            "assertions": [],
            "request": {
                "headers": {},
                "method": "GET",
                "url": api["url"],
            },
            "setCookie": "",
            "variables": [],
        },
        "locations": locations,
        "message": "{} {} {} browser check failed.\n{}".format(
            project, tier, api["name"], notification
        ),
        "name": monitor_name,
        "options": {
            "tick_every": freq,
            "device_ids": ["laptop_large"],
        },
        "status": "live",
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "type": "browser",
    }

    public_id = dd_client.find_synthetic_test(monitor_name)
    if public_id:
        print("{} already exists, updating with latest configuration.".format(monitor_name))
    else:
        print("{} not found, creating.".format(monitor_name))

    public_id = dd_client.upsert_synthetic_test(public_id, "browser", payload)
    print("{} upserted (public_id: {}).".format(monitor_name, public_id))
    return public_id
