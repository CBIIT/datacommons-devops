locals {
  http_port = 80
  any_port = 0
  any_protocol = "-1"
  tcp_protocol = "tcp"
  https_port = "443"
  all_ips  = ["0.0.0.0/0"]
  domain_name = "${var.stack_name}-${var.env}-elasticsearch"
}

resource "aws_security_group" "es" {
  name = "${var.stack_name}-${var.env}-elasticsearch-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port = local.https_port
    to_port = local.https_port
    protocol = local.tcp_protocol
    cidr_blocks = var.allowed_subnet_ip_block
  }
}

resource "aws_security_group_rule" "all_outbound" {
  from_port = local.any_port
  protocol = local.any_protocol
  to_port = local.any_port
  cidr_blocks = local.all_ips

  security_group_id = aws_security_group.es.id
  type = "egress"
}

resource "aws_iam_service_linked_role" "es" {
  count = var.create_es_service_role ? 1: 0
  aws_service_name = "es.amazonaws.com"
}

resource "aws_elasticsearch_domain" "es" {
  domain_name = local.domain_name
  elasticsearch_version = var.elasticsearch_version
  vpc_options {
    subnet_ids = var.private_subnet_ids
    security_group_ids = [aws_security_group.es.id]
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 120
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
    automated_snapshot_start_hour = 23
  }
  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.cloudwatch_log_group.arn
    log_type                 = "INDEX_SLOW_LOGS"
  }
  tags = var.tags
}


resource "aws_cloudwatch_log_group" "cloudwatch_log_group" {
  name = "${var.stack_name}-${var.env}-es-log-group"
}
