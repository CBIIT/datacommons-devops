data "aws_region" "region" {}

data "aws_caller_identity" "caller" {}

data "aws_iam_policy_document" "os_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:PutLogEvents",
      "logs:PutLogEventsBatch",
      "logs:CreateLogStream"
    ]
    principals {
      type        = "Service"
      identifiers = ["es.amazonaws.com"]
    }
    resources = [
      aws_cloudwatch_log_group.os_logs.arn,
      "${aws_cloudwatch_log_group.os_logs.arn}:*"
    ]
  }
}
