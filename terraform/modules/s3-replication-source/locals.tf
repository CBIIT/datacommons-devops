locals {
  role_name               = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-s3-replication-role" : "${var.resource_prefix}-s3-replication-role"
  policy_name             = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-s3-replication-policy" : "${var.resource_prefix}-s3-replication-policy"
  source_bucket_arn       = var.create_source_bucket ? aws_s3_bucket.source[0].arn : data.aws_s3_bucket.source[0].arn
  permission_boundary_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
}