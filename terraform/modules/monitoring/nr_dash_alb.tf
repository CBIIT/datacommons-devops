
resource "newrelic_one_dashboard" "alb_dashboard" {
  name = "${var.app} TEST ALB"
  permissions = "public_read_write"

  page {
    name = "AWS ALB"

    widget_line {
      title = "Requests, by ALB"
      row = 1
      column = 1
      height = 3
      width = 8

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT sum(`aws.applicationelb.RequestCount.byAlb`) from Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' TIMESERIES FACET  entityName UNTIL 6 minutes ago
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
![AWS ALB Icon](https://integrations.nr-assets.net/providers/aws_alb.png) **AWS ALB** 

An Application Load Balancer is a load balancing option for the Elastic Load Balancing service that operates at the application layer and allows you to define routing rules based on content across multiple services or containers running on one or more Amazon Elastic Compute Cloud (Amazon EC2) instances.





EOT
    }

    widget_billboard {
      title = "Backend Response Time"
      row = 4
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.applicationelb.TargetResponseTime`) as 'seconds' FROM Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%'
EOT
      }
    }

    widget_line {
      title = "HTTP Request Errors"
      row = 4
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT sum(`aws.applicationelb.HTTPCode_ELB_3XX_Count`) as '300 errors (backend)', sum(`aws.applicationelb.HTTPCode_ELB_4XX_Count`) as '400 errors (backend)', sum(`provider.HTTPCode_ELB_5XX_Count`) as '500 errors (backend)', sum(`provider.HTTPCodeElb4XXCount`) as '400 errors (frontend)', sum(`provider.HTTPCodeElb5XXCount`) as '500 errors (frontend)' FROM Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' TIMESERIES UNTIL 6 minutes ago
EOT
      }
    }

    widget_billboard {
      title = "Requests per second (ALB)"
      row = 7
      column = 5
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT rate(sum(`aws.applicationelb.RequestCount.byAlb`), 1 minute) as 'requests/second' FROM Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' since 60 minutes ago
EOT
      }
    }

    widget_billboard {
      title = "Requests per second (target group)"
      row = 7
      column = 9
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT rate(sum(`aws.applicationelb.RequestCount.byTargetGroup`), 1 minute) as 'requests/second' FROM Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' since 60 minutes ago
EOT
      }
    }

    widget_line {
      title = "Average Backend Response Time, by target group"
      row = 10
      column = 1
      height = 3
      width = 12

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT average(`aws.applicationelb.TargetResponseTime`) FROM Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' TIMESERIES facet entityName UNTIL 6 minutes ago
EOT
      }
    }

    widget_bar {
      title = "ALBs, by region"
      row = 13
      column = 1
      height = 3
      width = 4

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT uniqueCount(entity.id) from Metric WHERE collector.name='cloudwatch-metric-streams' and aws.Namespace = 'AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' facet aws.region
EOT
      }
    }

    widget_line {
      title = "HTTP Requests per second, by region"
      row = 13
      column = 5
      height = 3
      width = 8

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT sum(`aws.applicationelb.RequestCount.byAlb`) from Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace='AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' TIMESERIES FACET aws.region UNTIL 6 minutes ago
EOT
      }
    }

    widget_line {
      title = "Connection count"
      row = 16
      column = 1
      height = 3
      width = 12

      nrql_query {
        account_id = 2292606
        query = <<EOT
SELECT sum(`aws.applicationelb.ActiveConnectionCount`) as 'active', sum(`aws.applicationelb.NewConnectionCount`) as 'new', sum(`aws.applicationelb.RejectedConnectionCount`) as 'rejected' FROM Metric WHERE collector.name='cloudwatch-metric-streams' AND aws.Namespace = 'AWS/ApplicationELB' AND entity.name LIKE '%${var.app}%' TIMESERIES UNTIL 6 minutes ago
EOT
      }
    }
  }
}
