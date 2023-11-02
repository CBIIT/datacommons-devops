resource "aws_iam_role" "lambda_role" {
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_policy.json
  name =  local.lambda_role_name
  tags =  var.tags
  #permissions_boundary = var.target_account_cloudone ? local.permission_boundary_arn: null
}

resource "aws_iam_policy" "lambda_iam_policy" {
  policy = data.aws_iam_policy_document.lambda_s3_policy.json
  name = local.lambda_policy_name
}

resource "aws_iam_policy" "cloudwatch_log_iam_policy" {
  policy = data.aws_iam_policy_document.lambda_exec_role_policy.json
  name   = local.cloudwatch_policy_name
}

resource "aws_iam_policy_attachment" "lambda_s3_policy_attachment" {
  name = "${var.stack_name}-${var.env}-lambda-s3-attachement"
  policy_arn = aws_iam_policy.lambda_iam_policy.arn
  roles = [aws_iam_role.lambda_role.name]
}

resource "aws_iam_policy_attachment" "cloudwatch_log_policy_attachment" {
  name = "${var.stack_name}-${var.env}-cloudwatch-log-attachement"
  policy_arn = aws_iam_policy.cloudwatch_log_iam_policy.arn
  roles = [aws_iam_role.lambda_role.name]
}

resource "aws_lambda_function" "slack_lambda" {
  filename = "${path.module}/send-slack.zip"
  function_name = "${var.stack_name}-${var.env}-send-slack"
  role = aws_iam_role.lambda_role.arn
  handler = "slack.handler"
  memory_size = 512
  timeout = 60
  source_code_hash = filebase64sha256("${path.module}/send-slack.zip")
  runtime = "python3.8"
  environment {
    variables = {
      SLACK_URL = jsondecode(data.aws_secretsmanager_secret_version.slack_url.secret_string)[var.slack_url_secret_key]
      SLACK_CHANNEL = var.cloudfront_slack_channel_name
      REGION = data.aws_region.current.name
    }
  }

}

resource "aws_lambda_permission" "lambda_invoke_sns" {
  statement_id  = "allow_sns_function_invocation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slack_lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.cloudfront_alarm_topic.arn
}

resource "aws_lambda_function" "slack_waf" {
  filename = "${path.module}/wafreport.zip"
  function_name = "${var.stack_name}-${var.env}-waf-report"
  role = aws_iam_role.lambda_role.arn
  handler = "blocked.handler"
  memory_size = 1024
  timeout = 60
  source_code_hash = filebase64sha256("${path.module}/wafreport.zip")

  runtime = "python3.8"

  environment {
    variables = {
      SLACK_URL = jsondecode(data.aws_secretsmanager_secret_version.slack_url.secret_string)[var.slack_url_secret_key]
      SLACK_CHANNEL = var.cloudfront_slack_channel_name
      BLOCK_IP_FILE_NAME = "blocked_ip/ips.txt"
      WAF_SCOPE = "CLOUDFRONT"
      #S3_BUCKET_NAME = aws_s3_bucket.kinesis_log.bucket
      TMP_FILE_NAME = "/tmp/blocked_ip.txt"
      IP_SETS_NAME = aws_wafv2_ip_set.ip_sets.name
    }
  }
}

resource "aws_cloudwatch_event_rule" "every_7am" {
  name = "${var.stack_name}-${var.env}-every-7am"
  description = "run waf report every 7am"
  schedule_expression = "cron(0 7 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "run_waf_report_every_7am" {
  rule = aws_cloudwatch_event_rule.every_7am.name
  target_id = "${var.stack_name}-${var.env}-waf-report"
  arn = aws_lambda_function.slack_waf.arn
}

resource "aws_lambda_permission" "cloudwatch_invoke_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slack_waf.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.every_7am.arn
}
