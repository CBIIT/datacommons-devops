"""
monitors/downtime/set_recurring_downtime.py

Schedules (or updates) a recurring Datadog downtime for a single monitor,
identified by monitor_id. Designed to be called once per CSV row, right
after that row's synthetic test / metric monitor has been created and its
ID is known.

Uses the Datadog v2 Downtime API:
  https://docs.datadoghq.com/api/latest/downtimes/

Idempotency:
  Datadog's downtime API has no "upsert" — POSTing twice creates two
  downtimes. Before creating, we GET all downtimes and look for one that
  already targets this monitor_id with a recurring schedule. If found, we
  PATCH it instead of creating a duplicate.
"""

import os
import requests

DD_SITE = os.getenv("DD_SITE", "datadoghq.com")
BASE_URL = "https://api.{}/api/v2/downtime".format(DD_SITE)
SYNTHETICS_URL = "https://api.{}/api/v1/synthetics/tests".format(DD_SITE)

def _headers():
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": os.environ["DD_API_KEY"],
        "DD-APPLICATION-KEY": os.environ["DD_APP_KEY"],
    }

def _resolve_monitor_id(identifier):
    """
    The Downtime API's monitor_identifier.monitor_id field needs the
    numeric monitor ID Datadog auto-creates behind every monitor/synthetic
    test — NOT a Synthetics public_id string (e.g. "dqp-fwf-y5c").

    If `identifier` is already an int (or a numeric string), it's assumed
    to be a real monitor_id and is returned as-is. Otherwise it's treated
    as a Synthetics public_id and resolved via GET /synthetics/tests/{id},
    whose response includes the underlying numeric "monitor_id".
    """
    if isinstance(identifier, int):
        return identifier

    identifier = str(identifier)
    if identifier.isdigit():
        return int(identifier)

    # Treat as a Synthetics public_id and look up its numeric monitor_id.
    resp = requests.get(
        "{}/{}".format(SYNTHETICS_URL, identifier), headers=_headers()
    )
    if not resp.ok:
        print(
            "  WARNING: could not resolve monitor_id for synthetics "
            "public_id {} ({}): {}".format(identifier, resp.status_code, resp.text)
        )
        return None

    data = resp.json()
    monitor_id = data.get("monitor_id")
    if monitor_id is None:
        print(
            "  WARNING: synthetics test {} has no monitor_id in its "
            "response — cannot schedule downtime.".format(identifier)
        )
        return None

    return monitor_id

def _find_existing_downtime(monitor_id):
    """
    Look for an existing recurring downtime already scoped to this monitor_id.
    Returns the downtime's id if found, else None.

    NOTE: this does a full list-and-scan, which is fine for CSV-sized batch
    runs (dozens to low hundreds of monitors) but would need pagination
    handling for very large accounts. Check response["meta"] for pagination
    cursors if you hit scale issues.
    """
    resp = requests.get(BASE_URL, headers=_headers())
    resp.raise_for_status()
    downtimes = resp.json().get("data", [])

    for dt in downtimes:
        attrs = dt.get("attributes", {})
        identifier = attrs.get("monitor_identifier") or {}
        if identifier.get("monitor_id") == monitor_id and attrs.get("schedule", {}).get(
            "recurrences"
        ):
            return dt["id"]
    return None


def _build_rrule(days_of_week=None):
    """
    Build an RRULE string for a daily (or specific-weekday) recurrence.

    days_of_week: optional list like ["MO","TU","WE","TH","FR"]. If omitted,
    recurs every day.
    """
    if days_of_week:
        return "FREQ=WEEKLY;BYDAY={}".format(",".join(days_of_week))
    return "FREQ=DAILY;INTERVAL=1"


def _duration_string(start_hhmm, end_hhmm):
    """
    Compute an ISO-8601-ish duration string (e.g. "12h", "12h30m") from
    HH:MM start/end strings, assuming the window may cross midnight
    (e.g. 19:00 -> 07:00 is a 12-hour span).
    """
    sh, sm = (int(x) for x in start_hhmm.split(":"))
    eh, em = (int(x) for x in end_hhmm.split(":"))

    start_minutes = sh * 60 + sm
    end_minutes = eh * 60 + em

    if end_minutes <= start_minutes:
        # window crosses midnight
        end_minutes += 24 * 60

    total_minutes = end_minutes - start_minutes
    hours, minutes = divmod(total_minutes, 60)

    if minutes:
        return "{}h{}m".format(hours, minutes)
    return "{}h".format(hours)


def setdowntime(
    monitor_id,
    downtime_start,
    downtime_end,
    timezone,
    message="",
    days_of_week=None,
    start_date=None,
):
    """
    Schedule a recurring downtime for a single monitor.

    Args:
        monitor_id (int): Datadog monitor or synthetics test's numeric monitor ID.
        downtime_start (str): "HH:MM" 24-hour start time, e.g. "19:00".
        downtime_end (str): "HH:MM" 24-hour end time, e.g. "07:00".
        timezone (str): IANA tz name, e.g. "America/New_York".
        message (str): optional note shown on the downtime.
        days_of_week (list[str] or None): e.g. ["MO","TU","WE","TH","FR"].
            None means every day.
        start_date (str or None): "YYYY-MM-DD" for the first occurrence.
            Defaults to today's date in the given timezone if not provided —
            but since we don't do tz math here, pass it explicitly from the
            CSV/caller if "today" matters; otherwise Datadog will reject a
            start time that's already in the past for a one-off, though for
            recurring schedules a past first-occurrence date is fine and it
            simply starts counting from the next valid recurrence.
    """
    if not monitor_id:
        print("  Skipping downtime — no monitor_id provided.")
        return None

    resolved_id = _resolve_monitor_id(monitor_id)
    if not resolved_id:
        print(
            "  Skipping downtime — could not resolve a numeric monitor_id "
            "from {!r}.".format(monitor_id)
        )
        return None
    monitor_id = resolved_id

    if not downtime_start or not downtime_end:
        print("  Skipping downtime — Downtime_Start/Downtime_End not set in CSV.")
        return None

    duration = _duration_string(downtime_start, downtime_end)
    rrule = _build_rrule(days_of_week)

    # Datadog wants a naive local datetime (no offset) here; the separate
    # "timezone" field tells it how to interpret it.
    if not start_date:
        raise ValueError(
            "start_date is required (YYYY-MM-DD) — pass today's date in the "
            "target timezone from the caller."
        )
    start_dt = "{}T{}:00".format(start_date, downtime_start)

    payload = {
        "data": {
            "type": "downtime",
            "attributes": {
                "monitor_identifier": {"monitor_id": monitor_id},
                "scope": "*",
                "display_timezone": timezone,
                "message": message,
                "mute_first_recovery_notification": False,
                "notify_end_types": [],
                "schedule": {
                    "timezone": timezone,
                    "recurrences": [
                        {
                            "start": start_dt,
                            "duration": duration,
                            "rrule": rrule,
                        }
                    ],
                },
            },
        }
    }

    existing_id = _find_existing_downtime(monitor_id)

    if existing_id:
        payload["data"]["id"] = existing_id
        print(
            "  Updating existing downtime {} for monitor {}".format(
                existing_id, monitor_id
            )
        )
        resp = requests.patch(
            "{}/{}".format(BASE_URL, existing_id),
            headers=_headers(),
            json=payload,
        )
    else:
        print("  Creating new downtime for monitor {}".format(monitor_id))
        resp = requests.post(BASE_URL, headers=_headers(), json=payload)

    if not resp.ok:
        print(
            "  WARNING: downtime request failed ({}): {}".format(
                resp.status_code, resp.text
            )
        )
        return None

    resp.raise_for_status()
    return resp.json()["data"]["id"]
