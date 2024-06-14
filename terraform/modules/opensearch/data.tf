data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "logs" {
  count = var.create_cloudwatch_log_policy ? 1 : 0

  statement {
    effect = "Allow"
    actions = [
      "logs:PutLogEvents",
      "logs:CreateLogStream"
    ]
    principals {
      type        = "Service"
      identifiers = ["es.amazonaws.com"]
    }
    resources = [
      "${aws_cloudwatch_log_group.this[0].arn}",
      "${aws_cloudwatch_log_group.this[0].arn}:*"
    ]
  }
}

data "aws_iam_policy_document" "access_policy" {
  #count = var.create_access_policies ? 1 : 0

  statement {
    effect = "Allow"
    actions = [
      "es:ESHttpPut",
      "es:ESHttpPost",
      "es:ESHttpPatch",
      "es:ESHttpHead",
      "es:ESHttpGet",
      "es:ESHttpDelete"
    ]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    resources = ["${aws_opensearch_domain.this.arn}/*"]
  }
}

data "aws_iam_policy_document" "trust" {
  count = var.create_snapshot_role ? 1 : 0

  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["es.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "snapshot" {
  count = var.create_snapshot_role ? 1 : 0

  statement {
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [var.s3_snapshot_bucket_arn]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    resources = ["${var.s3_snapshot_bucket_arn}/*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "iam:PassRole",
      "iam:GetRole"
    ]
    resources = [aws_iam_role.snapshot[0].arn]
  }

  statement {
    effect  = "Allow"
    actions = ["es:ESHttpPut"]
    resources = [
      "${aws_opensearch_domain.this.arn}/*",
      "${aws_opensearch_domain.this.arn}/*/*"
    ]
  }
}
