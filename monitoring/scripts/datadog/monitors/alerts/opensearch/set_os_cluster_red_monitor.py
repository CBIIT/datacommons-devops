#!/usr/bin/python
"""
DataDog metric alert monitor: OpenSearch cluster status red.

Replaces: New Relic NRQL condition (the only active OpenSearch condition)
  FROM Metric SELECT min(aws.es.ClusterStatus.red)
  WHERE entity.name = '{project}-{tier}-opensearch'
  > 0 (critical, 1 min)

DataDog metric: aws.es.cluster_statusred
  Sourced from the DataDog AWS CloudWatch integration for Amazon OpenSearch
  (legacy Elasticsearch) service. A value > 0 means at least one primary shard
  and its replicas are not allocated to any node — the cluster is in red status.
  Tag filter: domain_name scoped to the project+tier domain.
"""

from monitors import dd_client


def setmonitor(project, tier, notification):
    monitor_name = "{} {} Opensearch Cluster Red".format(project, tier)
    domain_filter = "domain_name:{}-{}-opensearch".format(
        project.lower(), tier.lower()
    )

    payload = {
        "name": monitor_name,
        "type": "metric alert",
        # Use a 1-minute window to match NR critical_duration of 1
        "query": "max(last_1m):max:aws.es.cluster_statusred{{{filter}}} > 0".format(
            filter=domain_filter
        ),
        "message": (
            "OpenSearch cluster is in RED status for {project} {tier}. "
            "Primary shards are unallocated — data may be inaccessible.\n{notification}"
        ).format(project=project, tier=tier, notification=notification),
        "tags": [
            "project:{}".format(project.lower()),
            "tier:{}".format(tier.lower()),
        ],
        "priority": 1,
        "options": {
            "thresholds": {
                "critical": 0,
            },
            "notify_no_data": False,
            "evaluation_delay": 60,
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
