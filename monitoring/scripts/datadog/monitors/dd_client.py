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


def synthetics_location(location= "private"):
    """
    Decide which Datadog location a synthetic test should run from.

    Driven entirely by the CSV's "Location" column:

        Location = Public   -> Datadog's managed location
        Location = Private  -> our private location inside the AWS network

    Set this on every row of FNL-Monitoring-List-datadog.csv. The value is
    not case-sensitive and surrounding spaces are ignored.

    A blank value defaults to Private. That is the safer default of the two:
    the private location sits inside the network and can still reach public
    endpoints, whereas a public location cannot reach internal-only hosts at
    all. A new row added without a Location therefore keeps working rather
    than failing the run.

    An unrecognised value still stops the run. A blank cell means "not filled
    in yet", but a value like 'privte' means someone intended something
    specific and mistyped it, and quietly treating that as a default could
    route a monitor to the wrong place.

    Returns a single-item list, which is the shape Datadog expects.
    """
    requested = (location or "").strip().lower()

    if requested in ("", "private"):
        return [PRIVATE_LOCATION_ID]

    if requested == "public":
        return [PUBLIC_LOCATION_ID]

    raise SystemExit(
        "Location is {!r} in the CSV. Expected 'Public' or 'Private' "
        "(leave blank to default to Private).".format(location)
    )


# Projects piloting the Layered Monitoring Strategy (v2.6, Layer 1). Only the
# projects listed here get the strategy's frequency, retry, failure duration,
# tags and extra API assertions; every other project's tests are built
# exactly as before. Add a project here once the pilot has been verified.
#
#   app / team   values for the app: and team: tags
#   services     CSV Endpoint_Name (lower case) -> service: tag value
#   api_checks   CSV Endpoint_Name (lower case) -> extra assertion bundles
#                added to that endpoint's API test (see pilot_api_assertions)
STRATEGY_PILOT = {
    "cbioportal": {
        "app": "cbioportal",
        "team": "devops",
        "services": {
            "portal": "cbio-site",
            "content": "cbio-frontend",
            "about": "cbio-about",
            "api": "cbio-backend",
        },
        "api_checks": {
            "api": ["json_content_type", "no_error_envelope", "response_time"],
            "about": ["json_content_type", "version_number"],
        },
    },
}

# Strategy L1: one fast retry ~5 s after a failure, then the test must keep
# failing for one full run interval (5 min prod, 15 min lower tiers) before it
# alerts. Datadog counts that time from the first failed run, so the alert
# fires on the 2nd consecutive failed run ("≥2 consecutive runs (or ≥3–5
# minutes)" in the strategy). One location is used, so persistence over time
# replaces the strategy's ">=2 of 3 locations" rule.
_PILOT_TICK = {"prod": 300, "other": 900}  # 5 min prod, 15 min lower tiers
_PILOT_RETRY = {"count": 1, "interval": 5000}  # interval in ms
_PILOT_RESPONSE_TIME_MS = 2000


def pilot_config(project):
    """The project's STRATEGY_PILOT entry, or None if it is not in the pilot."""
    return STRATEGY_PILOT.get((project or "").strip().lower())


def _pilot_tier_key(tier):
    return "prod" if tier.lower() == "prod" else "other"


def tick_every(tier, project=None):
    """
    Synthetic-test run interval.

    Pilot projects: 5 min in prod, 15 min elsewhere (strategy L1).
    Everyone else: 10 min in prod, 30 min elsewhere.
    """
    if pilot_config(project):
        return _PILOT_TICK[_pilot_tier_key(tier)]
    return 600 if tier.lower() == "prod" else 1800


def failure_options(project, tier):
    """
    Extra synthetic options for pilot projects: one fast retry plus
    min_failure_duration of one run interval (5 min prod, 15 min lower
    tiers). The time counts from the first failed run, so the alert fires on
    the 2nd consecutive failed run and a single failed run never alerts.
    Returns {} for non-pilot projects.
    """
    if not pilot_config(project):
        return {}
    return {
        "retry": dict(_PILOT_RETRY),
        "min_failure_duration": _PILOT_TICK[_pilot_tier_key(tier)],
    }


def synthetic_monitor_options():
    """
    Notification options shared by every synthetic test.

    "hide_all" sends only our custom message (built by
    build_synthetic_alert_message) plus the event link. It drops Datadog's
    default enriched content -- the "Your test failed at least once from
    location ..." text, tags, footers -- and hides the @email / @slack
    handles from the rendered message. The handles still trigger delivery.

    It does NOT remove the "Triggered: [Synthetics] <name>" title or the
    Slack integration's own "Tags" / "Notified" fields; those are set per
    channel in the Datadog Slack integration, not on the test.
    """
    return {"notification_preset_name": "hide_all"}


def default_tags(project, tier):
    """The project/tier tag pair every monitor is tagged with."""
    return [
        "project:{}".format(project.lower()),
        "tier:{}".format(tier.lower()),
    ]


def synthetic_test_name(project, tier, journey):
    """
    Datadog name of a synthetic test. Tests are matched by exact name on every
    sync, so changing this creates new tests: delete the old ones first.

    Pilot projects use the strategy's '<app> – <journey>' format, with the
    environment appended so the four tiers stay unique:
    'cbioportal – API (prod)'. Everyone else keeps
    '<PROJECT> <Tier> <journey> Monitor'.
    """
    config = pilot_config(project)
    if not config:
        return "{} {} {} Monitor".format(project, tier, journey)
    return "{} – {} ({})".format(config["app"], journey, tier.lower())


def synthetic_tags(project, tier, endpoint_name):
    """
    Tags for a synthetic test.

    Pilot projects use the strategy's tag standard: service, env, app, team,
    and tier:page (the test is allowed to notify -- every cBio test does
    today). Here tier: means notification tier, so the environment moves to
    env:. Everyone else keeps default_tags (project:, tier:<environment>).
    """
    config = pilot_config(project)
    if not config:
        return default_tags(project, tier)

    endpoint = (endpoint_name or "").strip().lower()
    service = config["services"].get(endpoint) or "{}-{}".format(
        config["app"], endpoint.replace(" ", "-")
    )
    return [
        "service:{}".format(service),
        "env:{}".format(tier.lower()),
        "app:{}".format(config["app"]),
        "team:{}".format(config["team"]),
        "tier:page",
    ]


def pilot_api_assertions(project, endpoint_name):
    """
    Extra API-test assertions for pilot projects, per the strategy's API
    checklist. Empty for non-pilot projects and for endpoints without
    api_checks. Bundles:

      json_content_type  response Content-Type contains application/json
                         (a proxy/WAF HTML error page fails)
      no_error_envelope  body does not contain an "error" JSON key/value
                         (a 200 response carrying an error body fails)
      response_time      responds in under 2 s (generous; catches slow but
                         working degradation)
      version_number     $.version looks like a version number, e.g.
                         1.4.0.2 (liveness only -- never proof of DB health)
    """
    config = pilot_config(project)
    if not config:
        return []

    checks = config.get("api_checks", {}).get((endpoint_name or "").strip().lower(), [])
    bundles = {
        "json_content_type": {
            "type": "header",
            "property": "content-type",
            "operator": "contains",
            "target": "application/json",
        },
        "no_error_envelope": {
            "type": "body",
            "operator": "doesNotContain",
            "target": '"error"',
        },
        "response_time": {
            "type": "responseTime",
            "operator": "lessThan",
            "target": _PILOT_RESPONSE_TIME_MS,
        },
        "version_number": {
            "type": "body",
            "operator": "validatesJSONPath",
            "target": {
                "jsonPath": "$.version",
                "operator": "matches",
                "targetValue": r"^\d+\.\d+",
            },
        },
    }
    return [dict(bundles[name]) for name in checks]


def dd_app_base():
    """
    Base URL of the Datadog web UI for the configured site.

    Single-label sites (datadoghq.com, datadoghq.eu, ddog-gov.com) are served
    from app.<site>; regional sites (us3.datadoghq.com, ...) are served from
    the site host itself.
    """
    site = dd_site()
    return "https://{}".format(site if site.count(".") >= 2 else "app." + site)


def build_synthetic_alert_message(monitor_name, endpoint, notification):
    """
    Standard Slack payload for every Datadog synthetic monitor:

        {{#is_alert}}
        🚨 {MONITOR_NAME} — ALARM
        {ENDPOINT} failing

        [View Monitor]({MONITOR_LINK})
        {{/is_alert}}

        {{#is_recovery}}
        ✅ {MONITOR_NAME} — Recovered
        {ENDPOINT}
        API check passing again.

        [View Monitor]({MONITOR_LINK})
        {{/is_recovery}}

        {NOTIFICATION}

    The link sits inside each block and the handles go last, after a blank
    line. If a handle sits on the same line as the link, Slack shows its
    leftover text right after "View Monitor".

    *monitor_name* is the test's own Datadog name (e.g. "CBIOPORTAL Dev
    Content Monitor"), so the Slack title always matches the monitor. It
    already carries project, tier and endpoint name; a generic
    "{PROJECT} {TIER} Browser Monitor" title cannot be used because several
    tests share a project/tier/type (e.g. CBIOPORTAL Portal and Content).

    *endpoint* is "<METHOD> <URL>" for API and browser tests (browser tests
    always load the page with GET) and the bare host for SSL tests, which
    make no HTTP request.

    *notification* is the @-handle line, e.g.
    "@team@example.gov @slack-<account>-<channel>". Email handles are
    "@<address>"; there is no "@email:" prefix in Datadog.

    Resolved when the alert fires:
      - ALARM vs Recovered: Datadog's {{#is_alert}} / {{#is_recovery}} blocks.
      - MONITOR_LINK: built from {{synthetics.attributes.test.id}}, so it
        points at whichever test fired. Datadog has no link variable for
        synthetic tests.

    Filled in when the monitor is created or updated, from the same values
    that set the monitor's tags and request:
      - MONITOR_NAME: built from the same project/tier values as the
        project:/tier: tags. Tags are stored in lower case and Datadog
        templates cannot upper-case them, so {{tags.project}} would print
        'crdc-hub' instead of 'CRDC-HUB'.
      - ENDPOINT: the test's request config.
    Every monitor goes through this one function, so no monitor has its own
    wording. Re-running the CSV sync picks up any tag or URL change.
    """
    link = "{}/synthetics/details/{{{{synthetics.attributes.test.id}}}}".format(
        dd_app_base()
    )

    return (
        "{{#is_alert}}\n"
        "🚨 %(title)s — ALARM\n"
        "%(endpoint)s failing\n"
        "\n"
        "[View Monitor](%(link)s)\n"
        "{{/is_alert}}\n"
        "\n"
        "{{#is_recovery}}\n"
        "✅ %(title)s — Recovered\n"
        "%(endpoint)s\n"
        "API check passing again.\n"
        "\n"
        "[View Monitor](%(link)s)\n"
        "{{/is_recovery}}\n"
        "\n"
        "%(notification)s"
    ) % {
        "title": monitor_name,
        "endpoint": endpoint,
        "link": link,
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