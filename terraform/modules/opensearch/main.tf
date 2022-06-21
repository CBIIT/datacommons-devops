resource "aws_iam_service_linked_role" "os" {
  count            = var.create_os_service_role ? 1 : 0
  aws_service_name = "es.amazonaws.com"
}

resource "aws_opensearch_domain" "os" {
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
    security_group_ids = [aws_security_group.os.id]
  }

  ebs_options {
    ebs_enabled = true
    volume_size = var.opensearch_ebs_volume_size
  }

  log_publishing_options {
    enabled                  = var.opensearch_logs_enabled
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.os.arn
    log_type                 = var.opensearch_log_type
  }

  snapshot_options {
    automated_snapshot_start_hour = var.automated_snapshot_start_hour
  }

  auto_tune_options {
    desired_state       = var.opensearch_autotune_desired_state
    rollback_on_disable = var.opensearch_rollback_on_autotune_disable

    maintenance_schedule {
      start_at                       = "2022-06-20T23:00:30-0400"
      cron_expression_for_recurrence = "0 59 23 ? 0 0"
      duration {
        unit  = "HOURS"
        value = 2
      }
    }
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "os" {
  name = "${local.domain_name}-logs"
  tags = var.tags
}

resource "aws_cloudwatch_log_resource_policy" "os" {
  policy_name     = "${local.domain_name}-log-policy"
  policy_document = data.aws_iam_policy_document.os.json
  tags            = var.tags
}

resource "aws_security_group" "os" {
  name        = "${local.domain_name}-securitygroup"
  description = "The security group regulating network access to the OpenSearch cluster"
  vpc_id      = var.vpc_id
  tags        = var.tags
}