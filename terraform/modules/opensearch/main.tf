resource "aws_iam_service_linked_role" "es" {
  count            = var.create_os_service_role ? 1 : 0
  aws_service_name = "es.amazonaws.com"
}

resource "aws_opensearch_domain" "es" {
  domain_name    = local.domain_name
  engine_version = var.opensearch_version


  cluster_config {
    instance_type          = var.opensearch_instance_type
    instance_count         = var.opensearch_instance_count
    zone_awareness_enabled = var.multi_az_enabled
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

  encrypt_at_rest {
    enabled = true
  }

  node_to_node_encryption {
    enabled = true
  }

  vpc_options {
    subnet_ids         = [element(var.opensearch_subnet_ids, 0)]
    security_group_ids = var.opensearch_security_group_ids
  }

  ebs_options {
    ebs_enabled = true
    volume_size = var.opensearch_ebs_volume_size
  }

  log_publishing_options {
    enabled                  = var.opensearch_logs_enabled
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.es.arn
    log_type                 = var.opensearch_log_type
  }

  snapshot_options {
    automated_snapshot_start_hour = var.automated_snapshot_start_hour
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "es" {
  name = "${local.domain_name}-logs"
}

resource "aws_cloudwatch_log_resource_policy" "es" {
  policy_name = "${local.domain_name}-log-policy"

  policy_document = <<CONFIG
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "es.amazonaws.com"
      },
      "Action": [
        "logs:PutLogEvents",
        "logs:PutLogEventsBatch",
        "logs:CreateLogStream"
      ],
      "Resource": "arn:aws:logs:*"
    }
  ]
}
CONFIG
}
