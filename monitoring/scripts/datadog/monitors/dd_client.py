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


# Where synthetic tests run from.
#
# PRIVATE: a Datadog Private Location agent installed on a host inside our AWS
# network. Required for any endpoint whose DNS only resolves internally (most
# Dev/Qa/Stage hosts). This replaces the New Relic private location we used
# before the migration -- see monitoring/locations/README.md.
#
# PUBLIC: a Datadog-managed location, i.e. Datadog's own infrastructure on the
# public internet. Only works for endpoints that are publicly reachable.
# This account is on the government site (DD_SITE=ddog-gov.com), so the
# managed location must be a GovCloud one; the commercial "aws:us-east-1"
# is not valid on that site.
#
# Both can be overridden with an environment variable, so the IDs can be
# rotated without a code change.
PRIVATE_LOCATION_ID = os.getenv(
    "DD_LOWER_TIER_PRIVATE_LOCATION_ID",
    "pl:datadog-lowerter-private-location-a4dfa43d0f1db3da041b9723807eba74",
)
PUBLIC_LOCATION_ID = os.getenv("DD_PUBLIC_LOCATION_ID", "aws:us-gov-west-1")

# Tiers treated as non-production by the legacy fallback below.
_LOWER_TIERS = ("dev", "qa", "stage", "perf")


def synthetics_location(private_flag, tier=None, location=None):
    """
    Decide which Datadog location a synthetic test should run from.

    Driven by the CSV's "location" column:

        location = Public   -> Datadog's managed location
        location = Private  -> our private location inside the AWS network

    Set this per row in FNL-Monitoring-List-datadog.csv. The value is not
    case-sensitive and surrounding spaces are ignored.

    An unrecognised value stops the run instead of guessing. A typo that
    silently routed an internal-only endpoint to a public location would
    create a monitor that can never pass and alerts forever, so it is safer
    to fail immediately and have the CSV corrected.

    If the column is left blank, the older behaviour applies: the tier decides
    (Dev/Qa/Stage/Perf use the private location, everything else uses
    DD_PRIVATE_LOCATION_ID). This is only a safety net for rows that have not
    been filled in yet -- prefer setting the column explicitly.

    Returns a single-item list, which is the shape Datadog expects.
    """
    requested = (location or "").strip().lower()

    if requested == "private":
        return [PRIVATE_LOCATION_ID]

    if requested == "public":
        return [PUBLIC_LOCATION_ID]

    if requested:
        raise SystemExit(
            "Unrecognised location {!r} in the CSV. Expected 'Public' or "
            "'Private'.".format(location)
        )

    # --- Fallback: "location" column is blank, so fall back to the tier. ---

    # Private_Location=FALSE meant "run from a public location" before the
    # location column existed.
    if str(private_flag).lower() != "true":
        return ["aws:us-east-1"]

    if tier and tier.strip().lower() in _LOWER_TIERS:
        return [PRIVATE_LOCATION_ID]

    loc = os.getenv("DD_PRIVATE_LOCATION_ID", "")
    if not loc:
        raise SystemExit(
            "DD_PRIVATE_LOCATION_ID is required for private-location tests."
        )
    return [loc]


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