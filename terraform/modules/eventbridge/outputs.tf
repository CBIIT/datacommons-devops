output "eventbridge_rule_name" {
  value = aws_eventbridge_rule.module_event.name
}

output "eventbridge_target_id" {
  value = aws_eventbridge_target.module_target.target_id
}
