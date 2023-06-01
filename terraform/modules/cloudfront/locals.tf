locals {
  s3_origin_id = "${var.stack_name}_files_origin_id"
  env_type =  var.env == "dev" || var.env == "qa" ? "nonprod" : "prod"
  kenesis_role_name       = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-firehose-role" : "${var.resource_prefix}-firehose-role"
  kenesis_policy_name     = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-firehose-policy" : "${var.resource_prefix}-firehose-policy"
  kenesis_bucket_name     = var.target_account_cloudone ? "cloudone-${var.resource_prefix}-kinesis-firehose-stream" : "${var.resource_prefix}-kinesis-firehose-stream"
  files_bucket_name       = var.target_account_cloudone ? "cloudone-${var.resource_prefix}-files" : "${var.resource_prefix}-files"
  files_bucket_tag        = var.target_account_cloudone ? "cloudone-${var.stack_name}-${local.env_type}-files" : "${var.stack_name}-${var.env}-files"
  lambda_role_name        = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-lambda-role" : "${var.resource_prefix}-lambda-role"
  lambda_policy_name      = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-lambda-policy" : "${var.resource_prefix}-lambda-policy"
  cloudwatch_policy_name  = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-cloudwatch-log-policy" : "${var.resource_prefix}-cloudwatch-log-policy"
  files_log_bucket_name   = var.create_files_bucket ? "${local.files_bucket_name}-cloudfront-logs" : "${data.aws_s3_bucket.files_bucket[0].bucket}-cloudfront-logs"
  permission_boundary_arn = var.env == "prod" || var.env == "stage" ? null : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
}
