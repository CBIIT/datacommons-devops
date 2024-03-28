resource "aws_cloudwatch_metric_alarm" "cloudfront_alarm" {
  for_each                  = var.alarms
  alarm_name                = "${var.resource_prefix}-${each.key}-cloudfront-alarm"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "5"
  metric_name               = each.value["name"]
  namespace                 = "AWS/CloudFront"
  period                    = "60"
  statistic                 = "Sum"
  threshold                 = each.value["threshold"]
  alarm_description         = "CloudFront alarm for ${each.value["name"]}"
  insufficient_data_actions = []
  dimensions = {
    DistributionId = aws_cloudfront_distribution.distribution.id
    Region         = "Global"
  }
  alarm_actions = [aws_sns_topic.cloudfront_alarm_topic.arn]
  ok_actions    = [aws_sns_topic.cloudfront_alarm_topic.arn]

  tags = merge(
    {
      "CreateDate" = timestamp()
    },
    var.tags,
  )

  lifecycle {
    ignore_changes = [
      tags["CreateDate"],
    ]
  }
}

resource "aws_sns_topic" "cloudfront_alarm_topic" {
  name = "${var.resource_prefix}-cloudfront-4xx-5xx-errors"

  tags = merge(
    {
      "CreateDate" = timestamp()
    },
    var.tags,
  )

  lifecycle {
    ignore_changes = [
      tags["CreateDate"],
    ]
  }
}

resource "aws_sns_topic_subscription" "subscribe_slack_endpoint" {
  endpoint               = aws_lambda_function.slack_lambda.arn
  protocol               = "lambda"
  endpoint_auto_confirms = true
  topic_arn              = aws_sns_topic.cloudfront_alarm_topic.arn
}

resource "aws_cloudwatch_log_group" "log_group_waf" {
  name              = "/aws/lambda/${aws_lambda_function.slack_waf.function_name}"
  retention_in_days = 30

  tags = merge(
    {
      "CreateDate" = timestamp()
    },
    var.tags,
  )

  lifecycle {
    ignore_changes = [
      tags["CreateDate"],
    ]
  }
}

resource "aws_cloudwatch_log_group" "log_group_slack" {
  name              = "/aws/lambda/${aws_lambda_function.slack_lambda.function_name}"
  retention_in_days = 30

  tags = merge(
    {
      "CreateDate" = timestamp()
    },
    var.tags,
  )

  lifecycle {
    ignore_changes = [
      tags["CreateDate"],
    ]
  }
}