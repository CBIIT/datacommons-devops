# Output for the EventBridge rule name
output "eventbridge_rule_name" {
  value = aws_cloudwatch_event_rule.module_event.name
  description = "The name of the EventBridge rule."
}

# Output for the ECS EventBridge target ID, conditionally output if ECS target is created
output "eventbridge_ecs_target_id" {
  value       = aws_cloudwatch_event_target.ecs_target[0].target_id
  description = "The ID of the EventBridge target for the ECS task."
  condition   = length(aws_cloudwatch_event_target.ecs_target) > 0
}

# Output for the Lambda EventBridge target ID, conditionally output if Lambda target is created
output "eventbridge_lambda_target_id" {
  value       = aws_cloudwatch_event_target.lambda_target[0].target_id
  description = "The ID of the EventBridge target for the Lambda function."
  condition   = length(aws_cloudwatch_event_target.lambda_target) > 0
}
