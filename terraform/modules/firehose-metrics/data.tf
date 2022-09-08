############################################################################################################
############  General Data Sources #########################################################################
############################################################################################################

data "aws_caller_identity" "current" {}

############################################################################################################
############  Kinesis Data Firehose IAM Resources  #########################################################
############################################################################################################

data "aws_iam_policy_document" "cw_stream_to_firehose_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["streams.metrics.cloudwatch.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "cw_stream_to_firehose" {
  statement {
    effect = "Allow"
    actions = [
      "firehose:PutRecord",
      "firehose:PutRecordBatch"
    ]
    resources = [ aws_kinesis_firehose_delivery_stream.kenisis.arn ]
  }
}

############################################################################################################
############  Kinesis Data Firehose IAM Resources  #########################################################
############################################################################################################

data "aws_iam_policy_document" "kinesis_assume_role" {
  statement {
    sid     = "FirehoseDeliveryStream"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["firehose.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [var.external_id]
    }
  }
}

data "aws_iam_policy_document" "kenisis" {
  statement {
    effect = "Allow"
    actions = [
      "s3:AbortMultipartUpload",
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads",
      "s3:PutObject"
    ]
    resources = [
      "${var.s3_bucket_arn}",
      "${var.s3_bucket_arn}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "kinesis:DescribeStream",
      "kinesis:GetShardIterator",
      "kinesis:GetRecords",
      "kinesis:ListShards"
    ]
    resources = ["arn:aws:kinesis:us-east-1:${var.account_id}:stream/*"]
  }
}