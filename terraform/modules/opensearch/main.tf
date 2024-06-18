resource "aws_opensearch_domain" "this" {
  domain_name     = "${var.resource_prefix}-opensearch"
  engine_version  = var.engine_version
  access_policies = local.access_policies
  tags            = var.tags

  cluster_config {
    instance_type  = local.custom_instance_type
    instance_count = var.zone_awareness_enabled ? (local.custom_instance_count * 2) : local.custom_instance_count

    zone_awareness_enabled = var.zone_awareness_enabled

    zone_awareness_config {
      availability_zone_count = var.zone_awareness_enabled ? 2 : null
    }

    dedicated_master_enabled = var.dedicated_master_enabled
    dedicated_master_count   = var.dedicated_master_enabled ? 3 : 0
    dedicated_master_type    = var.dedicated_master_enabled ? local.custom_instance_type : null

    warm_enabled = var.warm_enabled
    #warm_count   = var.warm_enabled ? 2 : 0
    warm_count   = var.warm_enabled ? 2 : null
    warm_type    = var.warm_enabled ? local.custom_instance_type : null

    cold_storage_options {
      enabled = var.cold_storage_enabled
    }
  }

  auto_tune_options {
    desired_state = var.auto_tune_enabled ? "ENABLED" : "DISABLED"
  }

  domain_endpoint_options {
    enforce_https       = var.enforce_https
    tls_security_policy = var.tls_security_policy
  }

  ebs_options {
    ebs_enabled = true
    volume_size = local.custom_volume_size
    volume_type = var.volume_type
  }

  encrypt_at_rest {
    enabled = var.encrypt_at_rest
  }

  dynamic "log_publishing_options" {
    for_each = var.log_types

    content {
      enabled                  = true
      cloudwatch_log_group_arn = aws_cloudwatch_log_group.this[0].arn
      #log_type                 = each.value
      log_type                 = log_publishing_options.value
    }
  }

  node_to_node_encryption {
    enabled = true
  }

  snapshot_options {
    automated_snapshot_start_hour = var.automated_snapshot_start_hour
  }

  # software_update_options {
  #   auto_software_update_enabled = var.auto_software_update_enabled
  # }

  vpc_options {
    subnet_ids         = var.subnet_ids
    security_group_ids = local.security_group_ids
  }
}

resource "aws_security_group" "this" {
  count = var.create_security_group ? 1 : 0

  name        = "${var.resource_prefix}-opensearch-security-group"
  description = "The security group for the ${var.resource_prefix}-opensearch OpenSearch domain"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.resource_prefix}-opensearch-security-group"
  }
}

resource "aws_security_group_rule" "this" {
  count = var.create_security_group ? 1 : 0

  security_group_id = aws_security_group.this[0].id
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_cloudwatch_log_group" "this" {
  count = length(var.log_types) > 0 ? 1 : 0

  name              = "/aws/opensearch-service/${var.resource_prefix}"
  retention_in_days = var.log_retention_in_days
  tags              = var.tags
}

resource "aws_cloudwatch_log_resource_policy" "this" {
  count = var.create_cloudwatch_log_policy ? 1 : 0

  policy_name     = "${var.resource_prefix}-opensearch-log-policy"
  policy_document = data.aws_iam_policy_document.logs[0].json
}

resource "aws_iam_role" "snapshot" {
  count = var.create_snapshot_role ? 1 : 0

  name                 = "${var.iam_prefix}-${var.resource_prefix}-opensearch-snapshot-role"
  description          = "The snapshot role for the ${var.resource_prefix}-opensearch domain"
  assume_role_policy   = data.aws_iam_policy_document.trust[0].json
  permissions_boundary = local.permissions_boundary
  tags                 = var.tags
}

resource "aws_iam_policy" "snapshot" {
  count = var.create_snapshot_role ? 1 : 0

  name        = "${var.iam_prefix}-${var.resource_prefix}-opensearch-snapshot-policy"
  description = "The snapshot policy for the ${var.resource_prefix}-opensearch domain"
  policy      = data.aws_iam_policy_document.snapshot[0].json
}

resource "aws_iam_role_policy_attachment" "snapshot" {
  count = var.create_snapshot_role ? 1 : 0

  role       = aws_iam_role.snapshot[0].name
  policy_arn = aws_iam_policy.snapshot[0].arn
}