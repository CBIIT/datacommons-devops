
data "aws_s3_bucket" "source" {
  count = var.create_source_bucket ? 0 : 1
  bucket = var.source_bucket_name
}

data "aws_s3_bucket" "dest" {
  count = var.create_destination_bucket ? 0 : 1
  bucket = var.destination_bucket_name
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
      "s3:GetBucketAcl",
      "s3:GetBucketPolicy",
      "s3:ListBucket"
    ]
    resources = [
     local.source_bucket_arn
    ]
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

data "aws_iam_policy_document" "dest" {
  count = var.enable_replication ? 1 : 0
  version = "2012-10-17"
  statement {
    sid    = "SetPermissionForObject"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [

      ]
    }
    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete"
    ]
    resources = ["${local.destination_bucket_arn}/*"]
  }
  statement {
    sid    = "SetPermissionsOnTheBucket"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        var.replication_role_arn
      ]
    }
    actions = [
      "s3:List*",
      "s3:GetBucketVersioning",
      "s3:PutBucketVersioning"
    ]
    resources = [local.destination_bucket_arn]
  }
  statement {
    sid    = "PermissionToPassObjectOwnership"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        var.replication_role_arn,
      ]
    }
    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete",
      "s3:ReplicateTags",
      "s3:PutObject",
      "s3:ObjectOwnerOverrideToBucketOwner",
      "s3:GetObjectVersionTagging",
      "s3:GetObjectVersionForReplication",
    ]
    resources = ["${local.destination_bucket_arn}/*"]
  }

  }
