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
    tls_security_policy = var.opensearch_tls_policy
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

  dynamic "log_publishing_options" {
    for_each = var.opensearch_log_types
    iterator = i

    content {
      enabled                  = true
      cloudwatch_log_group_arn = aws_cloudwatch_log_group.os.arn
      log_type                 = i.value
    }
  }

  snapshot_options {
    automated_snapshot_start_hour = var.automated_snapshot_start_hour
  }

  tags = var.tags

}

resource "aws_cloudwatch_log_group" "os" {
  name              = "${local.domain_name}-logs"
  retention_in_days = local.log_retention
  tags              = var.tags
}

resource "aws_cloudwatch_log_resource_policy" "os" {
  count = var.create_cloudwatch_log_policy ? 1: 0
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
