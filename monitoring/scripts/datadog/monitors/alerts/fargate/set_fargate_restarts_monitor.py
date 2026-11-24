#!/usr/bin/python
"""
DataDog metric alert monitor: ECS Fargate container restarts.

Replaces: New Relic NRQL condition
  FROM ContainerSample SELECT max(restartCount)
  WHERE docker.ecsClusterName LIKE '{project}-{tier}-%'
  > 5 (critical)

DataDog metric: container.restarts
  Available when using the DataDog Agent v2 container check as an ECS Fargate
  sidecar. The metric counts the number of times a container has been
  restarted within the evaluation window.

  If the DataDog Agent is not deployed as a Fargate sidecar, adjust the query
  to use aws.ecs.service.running_task_count (alert on drops) or another
  available proxy metric.
"""

from monitors import dd_client


def setmonitor(project, tier, notification):
    monitor_name = "{} {} Fargate Container Restarts".format(project, tier)
    cluster_filter = "ecs_cluster_name:{}-{}*".format(
        project.lower(), tier.lower()
    )

    payload = {
        "name": monitor_name,
        "type": "metric alert",
        "query": "max(last_5m):max:container.restarts{{{filter}}} > 5".format(
            filter=cluster_filter
        ),
        "message": (
            "ECS Fargate containers in {project} {tier} have restarted more than 5 times.\n"
            "{notification}"
        ).format(project=project, tier=tier, notification=notification),
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "priority": 1,
        "options": {
            "thresholds": {
                "critical": 5,
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
