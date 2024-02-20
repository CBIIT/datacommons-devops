locals {
  sns_topic_arn = "arn:aws:sns:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${var.resource_prefix}-${var.sns_topic_name}"
}
