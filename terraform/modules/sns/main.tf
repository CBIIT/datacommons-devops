resource "aws_sns_topic" "main" {
  name        = "${var.resource_prefix}-${var.sns_topic_name}"
  display_name = var.sns_display_name
}

resource "aws_sns_topic_subscription" "slack" {
  topic_arn = aws_sns_topic.main.arn
  protocol  = "https"
  endpoint  = var.slack_webhook_url
}
