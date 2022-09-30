
resource "newrelic_one_dashboard" "os_dashboard" {
  name = "${var.app} TEST Opensearch"
  permissions = "public_read_write"

  page {
    name = "Amazon Elasticsearch Service"

    widget_line {
      title = "Green Cluster Status (min)"
      row = 1
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT min(`aws.es.ClusterStatus.green`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Yellow Cluster Status (min)"
      row = 1
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT min(`aws.es.ClusterStatus.yellow`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_markdown {
      title = ""
      row = 1
      column = 9
      height = 6
      width = 4
      text = <<EOT
![AWS Elasticsearch Icon](https://integrations.nr-assets.net/providers/aws_elasticsearch.png) **AWS Elasticsearch** 

Amazon Elasticsearch Service makes it easy to deploy, operate, and scale Elasticsearch for log analytics, full text search, application monitoring, and more. Amazon Elasticsearch Service is a fully managed service that delivers Elasticsearch’s easy-to-use APIs and real-time capabilities along with the availability, scalability, and security required by production workloads.





EOT
    }

    widget_line {
      title = "Red cluster Status (min)"
      row = 4
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT min(`aws.es.ClusterStatus.red`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average number of Nodes"
      row = 4
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.Nodes`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Search Rate"
      row = 7
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT sum(`aws.es.SearchRate.byNode`),sum(`aws.es.SearchRate.byCluster`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES auto SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "4xx requests"
      row = 7
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT sum(`aws.es.4xx`) as `4xx` FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES auto SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "5xx requests"
      row = 7
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT sum(`aws.es.5xx`) as `5xx` FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES auto SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average CPU utilization (%)"
      row = 10
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.CPUUtilization.byNode`) as `By Node`,average(`aws.es.CPUUtilization.byCluster`) as `By Cluster` FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Automatic snapshot failure"
      row = 10
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.AutomatedSnapshotFailure`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Max Cluster Used space (GiB)"
      row = 10
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT max(`aws.es.ClusterUsedSpace`) / 1024 FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Min Free storage space (GiB)"
      row = 13
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.FreeStorageSpace.byCluster`) / 1024 FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Max JVM memory pressure (%)"
      row = 13
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.JVMMemoryPressure.byNode`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Deleted documents"
      row = 13
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.DeletedDocuments`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Read latency (s)"
      row = 16
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.ReadLatency`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Read throughput (bytes/s)"
      row = 16
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.ReadThroughput`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Read IOPS"
      row = 16
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.ReadIOPS`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Write latency (s)"
      row = 19
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.WriteLatency`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Write throughput (bytes/s)"
      row = 19
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.WriteThroughput`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Write IOPS"
      row = 19
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.WriteIOPS`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Disk queue depth"
      row = 22
      column = 1
      height = 3
      width = 6

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.DiskQueueDepth`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Searchable documents"
      row = 22
      column = 7
      height = 3
      width = 6

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.SearchableDocuments`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Master JVM memory pressure (%)"
      row = 25
      column = 1
      height = 3
      width = 6

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.MasterJVMMemoryPressure`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }

    widget_line {
      title = "Average Master CPU Utilization (%)"
      row = 25
      column = 7
      height = 3
      width = 6

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.es.MasterCPUUtilization`) FROM  Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ES' AND aws.es.DomainName LIKE '${var.app}-%' TIMESERIES 1 minutes SINCE 1 hour ago UNTIL 5 minutes ago FACET entity.name
EOT
      }
    }
  }
}
