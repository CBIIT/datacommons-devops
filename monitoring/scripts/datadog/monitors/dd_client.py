#!/usr/bin/python
"""
Shared DataDog API helpers used by all monitor/synthetic modules.
"""

import os
import json

import requests


def dd_site():
    return os.getenv("DD_SITE", "datadoghq.com")


def dd_api_base():
    return "https://api.{}".format(dd_site())


def headers():
    return {
        "DD-API-KEY": os.getenv("DD_API_KEY"),
        "DD-APPLICATION-KEY": os.getenv("DD_APP_KEY"),
        "Content-Type": "application/json",
    }


def synthetics_location(private_flag):
    """Return a list with one DataDog location identifier."""
    if str(private_flag).lower() == "true":
        loc = os.getenv("DD_PRIVATE_LOCATION_ID", "")
        if not loc:
            raise SystemExit(
                "DD_PRIVATE_LOCATION_ID is required for private-location tests."
            )
        return [loc]
    return ["aws:us-east-1"]


def tick_every(tier):
    """Standard synthetic-test run interval: 10 min in prod, 30 min elsewhere."""
    return 600 if tier.lower() == "prod" else 1800


def default_tags(project, tier):
    """The project/tier tag pair every monitor is tagged with."""
    return [
        "project:{}".format(project.lower()),
        "tier:{}".format(tier.lower()),
    ]


def build_alarm_message(locations, description_alert, description_recovery, notification):
    """
    Shared State Change / Region / Description / notification skeleton used
    by every DataDog monitor's "message" field. *description_alert* and
    *description_recovery* are the already-filled-in sentences shown inside
    the {{#is_alert}}/{{#is_recovery}} blocks.
    """
    return (
        "**State Change**\n"
        "{{#is_recovery}}ALARM → OK{{/is_recovery}}{{#is_alert}}OK → ALARM{{/is_alert}}\n"
        "\n"
        "**Region**\n"
        "%(location)s\n"
        "\n"
        "Description\n"
        "{{#is_alert}}%(alert)s{{/is_alert}}\n"
        "{{#is_recovery}}%(recovery)s{{/is_recovery}}\n"
        "\n"
        "%(notification)s"
    ) % {
        "location": ", ".join(locations),
        "alert": description_alert,
        "recovery": description_recovery,
        "notification": notification,
    }


def find_synthetic_test(name):
    """
    Return the public_id of an existing DataDog synthetic test whose name
    exactly matches *name*, or None if not found.
    """
    try:
        response = requests.get(
            "{}/api/v1/synthetics/tests".format(dd_api_base()),
            headers=headers(),
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    for test in response.json().get("tests", []):
        if test.get("name") == name:
            return test.get("public_id")
    return None


def upsert_synthetic_test(public_id, test_type, payload):
    """
    Create or update a DataDog synthetic test.
    *test_type* is 'api' or 'browser' — used only for the create endpoint path.
    Returns the public_id of the upserted test.
    """
    h = headers()
    base = "{}/api/v1/synthetics/tests".format(dd_api_base())

    if public_id:
        # DataDog update endpoint: PUT /api/v1/synthetics/tests/{public_id}
        try:
            response = requests.put(
                "{}/{}".format(base, public_id),
                headers=h,
                data=json.dumps(payload),
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return public_id
    else:
        # DataDog create endpoint: POST /api/v1/synthetics/tests/api  (or /browser)
        endpoint = "{}/{}".format(base, test_type)
        try:
            response = requests.post(
                endpoint,
                headers=h,
                data=json.dumps(payload),
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response.json().get("public_id")


def upsert_and_report(monitor_name, test_type, payload):
    """
    Find-or-create + upsert + status prints, shared by every synthetic
    monitor module's setmonitor(). Returns the public_id.
    """
    public_id = find_synthetic_test(monitor_name)
    if public_id:
        print("{} already exists, updating with latest configuration.".format(monitor_name))
    else:
        print("{} not found, creating.".format(monitor_name))

    public_id = upsert_synthetic_test(public_id, test_type, payload)
    print("{} upserted (public_id: {}).".format(monitor_name, public_id))
    return public_id


def find_monitor(name):
    """
    Return the id of an existing DataDog metric monitor whose name exactly
    matches *name*, or None if not found.
    """
    try:
        response = requests.get(
            "{}/api/v1/monitor".format(dd_api_base()),
            headers=headers(),
            params={"name": name},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    for m in response.json():
        if m.get("name") == name:
            return m.get("id")
    return None


def upsert_monitor(monitor_id, payload):
    """
    Create or update a DataDog monitor. Returns the monitor id.
    """
    h = headers()
    base = "{}/api/v1/monitor".format(dd_api_base())

    if monitor_id:
        try:
            response = requests.put(
                "{}/{}".format(base, monitor_id),
                headers=h,
                data=json.dumps(payload),
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return monitor_id
    else:
        try:
            response = requests.post(
                base,
                headers=h,
                data=json.dumps(payload),
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return response.json().get("id")