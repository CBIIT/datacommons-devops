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
      "logs:PutRetentionPolicy"
    ]
    principals {
      type        = "Service"
      identifiers = ["es.amazonaws.com"]
    }
    resources = [
      "arn:aws:logs:${data.aws_region.region.name}:${data.aws_caller_identity.caller.account_id}:log-group:/aws/OpenSearchService/domains/*:*"
      # aws_cloudwatch_log_group.os.arn,
      # "${aws_cloudwatch_log_group.os.arn}:*"
    ]
  }
}
