locals {
  role_name           = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-s3-replication-role" : "${var.stack_name}-${var.env}-s3-replication-role"
  policy_name         = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-s3-replication-policy" : "${var.stack_name}-${var.env}-s3-replication-policy"
  source_bucket_arn   = var.create_source_bucket ? aws_s3_bucket.source[0].arn : data.aws_s3_bucket.source[0].arn
  destination_bucket_arn   = var.create_destination_bucket ? aws_s3_bucket.dest[0].arn : data.aws_s3_bucket.dest[0].arn
}