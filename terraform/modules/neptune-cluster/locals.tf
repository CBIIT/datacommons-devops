locals {
  create_parameter_groups = var.enable_serverless ? false : var.create_parameter_groups

  # outputs:
  kms_key_id     = var.create_kms_key ? aws_kms_key.this[0].key_id : "KMS was created by AWS"
  kms_alias_arn  = var.create_kms_key ? aws_kms_alias.this[0].arn : "KMS was created by AWS"
  kms_alias_id   = var.create_kms_key ? aws_kms_alias.this[0].id : "KMS was created by AWS"
  kms_alias_name = var.create_kms_key ? aws_kms_alias.this[0].name : "KMS was created by AWS"
}
