#!/usr/bin/python
"""
DataDog metric alert monitor: ALB target 5xx error count.

Replaces: New Relic NRQL condition
  FROM Metric SELECT sum(aws.applicationelb.HTTPCode_Target_5XX_Count)
  WHERE entity.name LIKE '%{project}-{tier}-lb%'
  > 1 (critical, 5 min)

DataDog metric: aws.applicationelb.httpcode_target_5xx
  Counts 5xx responses returned by the registered targets (not the load
  balancer itself), indicating application-level errors.
"""

from monitors import dd_client


def setmonitor(project, tier, notification):
    monitor_name = "{} {} ALB Target 5xx Count".format(project, tier)
    lb_filter = "loadbalancer:app/*{project}-{tier}*".format(
        project=project.lower(), tier=tier.lower()
    )

    payload = {
        "name": monitor_name,
        "type": "metric alert",
        "query": "sum(last_5m):sum:aws.applicationelb.httpcode_target_5xx{{{filter}}}.as_count() > 1".format(
            filter=lb_filter
        ),
        "message": (
            "ALB targets are returning 5xx errors for {project} {tier}.\n{notification}"
        ).format(project=project, tier=tier, notification=notification),
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "priority": 1,
        "options": {
            "thresholds": {
                "critical": 1,
            },
            "notify_no_data": False,
            "evaluation_delay": 120,
            "include_tags": True,
        },
    }

    monitor_id = dd_client.find_monitor(monitor_name)
    if monitor_id:
        print("{} already exists, updating with latest configuration.".format(monitor_name))
    else:
        print("{} not found, creating.".format(monitor_name))

    monitor_id = dd_client.upsert_monitor(monitor_id, payload)
    print("{} upserted (id: {}).".format(monitor_name, monitor_id))
    return monitor_id
