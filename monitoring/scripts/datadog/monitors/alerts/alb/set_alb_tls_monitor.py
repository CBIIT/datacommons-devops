#!/usr/bin/python
"""
DataDog metric alert monitor: ALB TLS negotiation errors.

Replaces: New Relic NRQL condition
  FROM Metric SELECT sum(aws.applicationelb.TargetTLSNegotiationErrorCount)
  WHERE entity.name LIKE '%{project}-{tier}-lb%'
  > 0 (critical, 5 min)

DataDog metric: aws.applicationelb.client_tls_negotiation_error_count
  Number of TLS connections initiated by the client that did not establish a
  session with the load balancer due to a TLS error.
"""

from monitors import dd_client


def setmonitor(project, tier, notification):
    monitor_name = "{} {} ALB TLS Negotiation Errors".format(project, tier)
    lb_filter = "loadbalancer:app/*{project}-{tier}*".format(
        project=project.lower(), tier=tier.lower()
    )

    payload = {
        "name": monitor_name,
        "type": "metric alert",
        "query": "sum(last_5m):sum:aws.applicationelb.client_tls_negotiation_error_count{{{filter}}}.as_count() > 0".format(
            filter=lb_filter
        ),
        "message": (
            "ALB TLS negotiation errors detected for {project} {tier}.\n{notification}"
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
