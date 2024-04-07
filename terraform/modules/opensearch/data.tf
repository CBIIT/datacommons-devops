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
      
      # aws_cloudwatch_log_group.os.arn,
      # arn:aws:logs:us-east-1:339649878709:log-group:cds-dev2-opensearch-logs:*
      "arn:aws:logs:*:*:*"
    ]
  }
}
