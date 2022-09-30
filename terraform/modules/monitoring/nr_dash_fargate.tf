
resource "newrelic_one_dashboard" "fargate_dashboard" {
  name = "${var.app}-${terraform.workspace} TEST Fargate"
  permissions = "public_read_only"

  page {
    name = "page_1"

    widget_markdown {
      title = ""
      row = 1
      column = 1
      height = 3
      width = 4
      text = <<EOT
This Dashboard provides an overview of Fargate resources for this tier.
EOT
    }

    widget_line {
      title = "Container Restarts"
      row = 1
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
FROM ContainerSample SELECT max(restartCount) - min(restartCount) WHERE ecsClusterName LIKE '${var.app}-${terraform.workspace}-%' TIMESERIES FACET ecsContainerName
EOT
      }
    }

    widget_line {
      title = "CPU Usage (cluster)"
      row = 1
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.ecs.CPUUtilization.byService`) as 'CPU utilization (%)' FROM Metric WHERE aws.ecs.ClusterName LIKE '${var.app}-${terraform.workspace}-%' TIMESERIES auto
EOT
      }
    }

    widget_line {
      title = "Memory Usage (%)  (cluster)"
      row = 7
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.ecs.MemoryUtilization.byService`) as 'Memory utilization (%)' FROM Metric WHERE aws.ecs.ClusterName LIKE '${var.app}-${terraform.workspace}-%' TIMESERIES auto
EOT
      }
    }

    widget_line {
      title = "Container CPU Cores Used (%)"
      row = 7
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
 FROM Metric SELECT average(`docker.container.cpuUsedCoresPercent`) as 'CPU cores (%)' WHERE docker.ecsClusterName LIKE '${var.app}-${terraform.workspace}-%' TIMESERIES auto FACET docker.ecsContainerName
EOT
      }
    }

    widget_bar {
      title = "Container Memory Used (average)"
      row = 7
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
FROM ContainerSample SELECT average(`memoryUsageBytes`) as 'Mem Used (bytes)' WHERE ecsClusterName LIKE '${var.app}-${terraform.workspace}-%' FACET ecsContainerName
EOT
      }
    }
  }
}
