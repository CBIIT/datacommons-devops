resource "aws_cloudwatch_event_rule" "scheduled_event" {
  name                = local.cloudwatch_event_rule_name
  description         = "Scheduled event rule"
  schedule_expression = var.cron_expression
}

resource "aws_cloudwatch_event_target" "event_target" {
  count     = var.target_type != "" ? 1 : 0
  rule      = aws_cloudwatch_event_rule.scheduled_event.name
  target_id = "custom-target"

  // The ARN and other parameters will be customize based on the target type
  dynamic "custom_target" {
    for_each = var.target_type == "custom" ? [1] : []
    content {
      arn = var.custom_target_arn
    }
  }
}

resource "aws_cloudwatch_event_permission" "events_permission" {
  count            = var.target_type != "" ? 1 : 0
  action          = "lambda:InvokeFunction"
  principal       = "events.amazonaws.com"
  source_arn      = aws_cloudwatch_event_rule.scheduled_event.arn
  statement_id    = "AllowInvoke"
  function_name   = aws_cloudwatch_event_target.event_target[0].arn
  source_profile  = aws_iam_role.events_role.arn
}

