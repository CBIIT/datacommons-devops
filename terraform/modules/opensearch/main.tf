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
    subnet_ids         = local.subnets
    security_group_ids = [aws_security_group.os.id]
  }

  ebs_options {
    ebs_enabled = true
    volume_size = var.opensearch_ebs_volume_size
  }

  # we can have multiple log_publishing_options blocks, one for each log type.
  # we should set-up a dynamic resource to create a block for each variable map passed to the module.
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
      start_at                       = local.autotune_start
      cron_expression_for_recurrence = local.autotune_reoccurance_cron
      duration {
        unit  = "HOURS"
        value = 2
      }
    }
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [
      "auto_tune_options[0].maintenance_schedule[0].start_at"

    ]
  }
}

resource "aws_cloudwatch_log_group" "os" {
  name              = "${local.domain_name}-logs"
  retention_in_days = local.log_retention
  tags              = var.tags
}

resource "aws_cloudwatch_log_resource_policy" "os" {
  policy_name     = "${local.domain_name}-log-policy"
  policy_document = data.aws_iam_policy_document.os.json
}

resource "aws_security_group" "os" {
  name                   = "${local.domain_name}-securitygroup"
  description            = local.sg_description
  revoke_rules_on_delete = true
  vpc_id                 = var.vpc_id
  tags                   = var.tags
}