
data "aws_caller_identity" "current" {}
data "aws_s3_bucket" "source" {
  count  = var.create_source_bucket ? 0 : 1
  bucket = var.source_bucket_name
}

data "aws_iam_policy_document" "main" {
  version = "2012-10-17"
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole",
    ]
    principals {
      type = "Service"
      identifiers = [
        "s3.amazonaws.com"
      ]
    }
  }
}

data "aws_iam_policy_document" "source" {
  version = "2012-10-17"
  statement {

    effect = "Allow"
    actions = [
      "s3:GetReplicationConfiguration",
      "s3:ListBucket"
    ]
    resources = [local.source_bucket_arn]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObjectVersionForReplication",
      "s3:GetObjectVersionAcl",
      "s3:GetObjectVersionTagging",
      "s3:GetObjectRetention",
      "s3:GetObjectLegalHold"
    ]
    resources = [
      "${local.source_bucket_arn}/*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete",
      "s3:ReplicateTags",
      "s3:ObjectOwnerOverrideToBucketOwner"
    ]
    resources = [
      "arn:aws:s3:::${var.destination_bucket_name}/*",
    ]
  }
}