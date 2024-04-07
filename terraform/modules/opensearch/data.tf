data "aws_region" "region" {}

data "aws_caller_identity" "caller" {}

data "aws_iam_policy_document" "os" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:PutMetricFilter",
      "logs:PutRetentionPolicy",
      "logs:*"
    ]
    principals {
      type        = "Service"
      identifiers = ["es.amazonaws.com"]
    }
    resources = [
      aws_cloudwatch_log_group.os.arn
    ]
  }
}
