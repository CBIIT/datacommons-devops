data "aws_s3_bucket" "dest" {
  count = var.create_destination_bucket ? 0 : 1
  bucket = var.destination_bucket_name
}

data "aws_iam_policy_document" "dest" {
  version = "2012-10-17"
  statement {
    sid    = "SetPermissionForObject"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        var.replication_role_arn
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
