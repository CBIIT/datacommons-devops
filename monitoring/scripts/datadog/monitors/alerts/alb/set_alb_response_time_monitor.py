#!/usr/bin/python
"""
DataDog metric alert monitor: ALB target response time.

Replaces: New Relic NRQL condition
  FROM Metric SELECT average(aws.applicationelb.TargetResponseTime)
  WHERE entity.name LIKE '%{project}-{tier}-lb%'
  > 0.4 seconds (critical, 5 min)

DataDog metric: aws.applicationelb.target_response_time.average
  Average response time (in seconds) for requests that elicited a response
  from an ALB target.
"""

from monitors import dd_client


def setmonitor(project, tier, notification):
    monitor_name = "{} {} ALB Target Response Time".format(project, tier)
    lb_filter = "loadbalancer:app/*{project}-{tier}*".format(
        project=project.lower(), tier=tier.lower()
    )

    payload = {
        "name": monitor_name,
        "type": "metric alert",
        "query": "avg(last_5m):avg:aws.applicationelb.target_response_time.average{{{filter}}} > 0.4".format(
            filter=lb_filter
        ),
        "message": (
            "ALB target response time is above 0.4s for {project} {tier}.\n{notification}"
        ).format(project=project, tier=tier, notification=notification),
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "priority": 2,
        "options": {
            "thresholds": {
                "critical": 0.4,
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
