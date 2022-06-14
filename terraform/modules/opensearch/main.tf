locals {
  domain_name = "${var.stack_name}-${var.env}-opensearch"
}

data "aws_region" "region" {}
data "aws_caller_identity" "caller" {}

resource "aws_iam_service_linked_role" "es" {
  count = var.create_os_service_role ? 1: 0
  aws_service_name = "es.amazonaws.com"
}

resource "aws_elasticsearch_domain" "es" {
  domain_name = local.domain_name
  elasticsearch_version = var.opensearch_version
  vpc_options {
    subnet_ids = [element(var.opensearch_subnet_ids,0)]
    security_group_ids = var.opensearch_security_group_ids
  }
  ebs_options {
    ebs_enabled = true
    volume_size = var.opensearch_ebs_volume_size
  }
  access_policies = <<CONFIG
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Action": "es:*",
          "Principal": "*",
          "Effect": "Allow",
          "Resource": "arn:aws:es:${data.aws_region.region.name}:${data.aws_caller_identity.caller.account_id}:domain/${local.domain_name}/*"
      }
  ]
}
  CONFIG
  snapshot_options {
    automated_snapshot_start_hour = var.automated_snapshot_start_hour
  }
  tags = var.tags
}

