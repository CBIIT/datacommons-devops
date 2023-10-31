data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_s3_bucket" "files_bucket" {
  count = var.create_files_bucket ? 0 : 1
  bucket = var.cloudfront_distribution_bucket_name
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = [var.create_files_bucket ?  "arn:aws:s3:::${local.files_bucket_name}/*" : "${data.aws_s3_bucket.files_bucket[0].arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.origin_access.iam_arn]
    }
  }
}

#get managed s3cors policy
data "aws_cloudfront_origin_request_policy" "s3_cors" {
  id = "88a5eaf4-2fd4-4709-b370-b4c650ea3fcf"
}

#get managed cloudfront distribution
data "aws_cloudfront_cache_policy" "managed_cache" {
  name = "Managed-CachingOptimized"
}

data "aws_iam_policy_document" "kinesis_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect = "Allow"
    sid = ""
    principals {
      identifiers = ["firehose.amazonaws.com"]
      type = "Service"
    }
  }
}

data "aws_iam_policy_document" "firehose_policy" {
  count  = var.create_kinesis ? 1:0
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "s3:AbortMultipartUpload",
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads",
      "s3:PutObject"
    ]
    #resources = [
      #aws_s3_bucket.kinesis_log.arn,
      #"${aws_s3_bucket.kinesis_log[0].arn}/*"
    #]
  }
  statement {
    effect = "Allow"
    sid = ""
    actions = ["iam:CreateServiceLinkedRole"]
    resources = ["arn:aws:iam::*:role/aws-service-role/wafv2.amazonaws.com/AWSServiceRoleForWAFV2Logging"]
  }
}
data "aws_secretsmanager_secret_version" "slack_url" {
  secret_id = var.slack_secret_name
}
data "aws_secretsmanager_secret_version" "cloudfront" {
  secret_id = "cloudfront"
}

data "aws_iam_policy_document" "lambda_assume_policy" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type = "Service"
    }
  }
}

data "aws_iam_policy_document" "lambda_s3_policy" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:GetObjectVersion",
    ]
    resources = ["arn:aws:s3:::${aws_s3_bucket.kinesis_log[count.index].bucket}/*"]
  }
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.kinesis_log.bucket}"
    ]
  }
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "wafv2:ListIPSets",
      "wafv2:UpdateIPSet",
      "wafv2:GetIPSet",

    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "lambda_exec_role_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }
}

