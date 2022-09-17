locals {
  s3_origin_id = "${var.stack_name}_files_origin_id"
  kenesis_role_name       = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-firehose-role" : "${var.stack_name}-${var.env}-firehose-role"
  kenesis_policy_name     = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-firehose-policy" : "${var.stack_name}-${var.env}-firehose-policy"
  kenesis_bucket_name     = var.target_account_cloudone ? "cloudone-${var.stack_name}-${var.env}-kinesis-firehose-stream" : "${var.stack_name}-${var.env}-kinesis-firehose-stream"
  lambda_role_name        = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-lambda-role" : "${var.stack_name}-${var.env}-lambda-role"
  lambda_policy_name      = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-lambda-policy" : "${var.stack_name}-${var.env}-lambda-policy"
  cloudwatch_policy_name  = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-cloudwatch-log-policy" : "${var.stack_name}-${var.env}-cloudwatch-log-policy"
}
