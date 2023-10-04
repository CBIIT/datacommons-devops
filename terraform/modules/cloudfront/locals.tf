locals {
  s3_origin_id = "${var.stack_name}_files_origin_id"
  env_type                = terraform.workspace
  kenesis_role_name       = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-firehose-role" : "${var.stack_name}-${var.env}-firehose-role"
  kenesis_policy_name     = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-firehose-policy" : "${var.stack_name}-${var.env}-firehose-policy"
  kenesis_bucket_name     = var.target_account_cloudone ? "cloudone-${var.stack_name}-${var.env}-kinesis-firehose-stream" : "${var.stack_name}-${var.env}-kinesis-firehose-stream"
  files_bucket_name       = var.target_account_cloudone ? "cloudone-${var.stack_name}-${local.env_type}-files" : "${var.stack_name}-${var.env}-files"
  lambda_role_name        = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-lambda-role" : "${var.stack_name}-${var.env}-lambda-role"
  lambda_policy_name      = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-lambda-policy" : "${var.stack_name}-${var.env}-lambda-policy"
  cloudwatch_policy_name  = var.target_account_cloudone ? "${var.iam_prefix}-${var.stack_name}-${var.env}-cloudwatch-log-policy" : "${var.stack_name}-${var.env}-cloudwatch-log-policy"
  files_log_bucket_name   = var.create_files_bucket ? "${local.files_bucket_name}-cloudfront-logs" : "${data.aws_s3_bucket.files_bucket[0].bucket}-cloudfront-logs"
  permission_boundary_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
  permissions_boundary = var.target_account_cloudone && terraform.workspace == "dev2" || terraform.workspace == "dev" || terraform.workspace =="qa" || terraform.workspace =="qa2" ? local.permission_boundary_arn: null
}
