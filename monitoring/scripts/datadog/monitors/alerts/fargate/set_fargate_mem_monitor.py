#!/usr/bin/python
"""
DataDog metric alert monitor: ECS Fargate memory utilisation.

Replaces: New Relic NRQL condition
  FROM Metric SELECT average(aws.ecs.MemoryUtilization)
  WHERE entity.name LIKE '{project}-{tier}-%'
  > 80% (critical, 5 min)

DataDog metric: aws.ecs.service.memory_utilization
  Collected via the DataDog AWS CloudWatch metric integration for ECS.
  This is a percentage value sourced directly from CloudWatch.
  Tag filter: cluster_name scoped to the project+tier cluster.
"""

from monitors import dd_client


def setmonitor(project, tier, notification):
    monitor_name = "{} {} Fargate Memory Usage".format(project, tier)
    cluster_filter = "cluster_name:{}-{}*".format(
        project.lower(), tier.lower()
    )

    payload = {
        "name": monitor_name,
        "type": "metric alert",
        "query": "avg(last_5m):avg:aws.ecs.service.memory_utilization{{{filter}}} > 80".format(
            filter=cluster_filter
        ),
        "message": (
            "ECS Fargate memory utilisation is critically high for {project} {tier}.\n"
            "Threshold: >80% over 5 minutes.\n{notification}"
        ).format(project=project, tier=tier, notification=notification),
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "priority": 1,
        "options": {
            "thresholds": {
                "critical": 80,
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
