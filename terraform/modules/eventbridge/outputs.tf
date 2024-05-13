output "eventbridge_rule_name" {
  value = aws_cloudwatch_event_rule.module_event.name
}

output "eventbridge_target_id" {
  value = aws_cloudwatch_event_target.module_target.target_id
}
