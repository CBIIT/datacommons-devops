output "cloudwatch_event_rule_arn" {
  value = aws_cloudwatch_event_rule.scheduled_event.arn
}

output "events_role_arn" {
  value = aws_iam_role.events_role[0].arn
}
