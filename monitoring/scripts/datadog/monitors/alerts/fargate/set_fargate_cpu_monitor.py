#!/usr/bin/python
"""
DataDog metric alert monitor: ECS Fargate CPU utilisation.

Replaces: New Relic NRQL condition
  FROM Metric SELECT average(docker.container.cpuUsedCoresPercent)
  WHERE docker.ecsClusterName LIKE '{project}-{tier}-%'
  > 90% (critical, 5 min) / > 80% (warning, 2 min)

DataDog metric: ecs.fargate.cpu.percent
  Collected by the DataDog Agent ECS Fargate integration. Available when the
  DataDog container agent is deployed as a sidecar in the task definition.
  Tag filter uses ecs_cluster_name scoped to the project+tier cluster.
"""

from monitors import dd_client


def setmonitor(project, tier, notification):
    monitor_name = "{} {} Fargate CPU Usage".format(project, tier)
    cluster_filter = "ecs_cluster_name:{}-{}*".format(
        project.lower(), tier.lower()
    )

    payload = {
        "name": monitor_name,
        "type": "metric alert",
        # avg over 5 min to match NR critical_duration of 5
        "query": "avg(last_5m):avg:ecs.fargate.cpu.percent{{{filter}}} > 90".format(
            filter=cluster_filter
        ),
        "message": (
            "ECS Fargate CPU usage is critically high for {project} {tier}.\n"
            "Threshold: >90% over 5 minutes.\n{notification}"
        ).format(project=project, tier=tier, notification=notification),
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "priority": 1,
        "options": {
            "thresholds": {
                "critical": 90,
                "warning": 80,
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
