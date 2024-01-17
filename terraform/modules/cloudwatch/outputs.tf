output "cloudwatch_event_rule_arn" {
  value = aws_cloudwatch_event_rule.ecs_scheduled_event.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.slack_notifications.arn
}

output "cloudwatch_events_role_arn" {
  value = aws_iam_role.cloudwatch_events_role.arn
}
