locals {
  account_arn = format("arn:aws:iam::%s:root", data.aws_caller_identity.current.account_id)
  ecr_repo_prefix = var.create_env_specific_repo ? "${var.stack_name}-${var.env}" : var.stack_name
}