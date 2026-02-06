# Output for the EventBridge rule name
output "eventbridge_rule_name" {
  value = aws_cloudwatch_event_rule.module_event.name
  description = "The name of the EventBridge rule."
}

# Output for the ECS EventBridge target ID, providing a default value if no resource is created
output "eventbridge_ecs_target_id" {
  value = length(aws_cloudwatch_event_target.ecs_target) > 0 ? aws_cloudwatch_event_target.ecs_target[0].target_id : "No ECS target created"
  description = "The ID of the EventBridge target for the ECS task."
}

# Output for the Lambda EventBridge target ID, providing a default value if no resource is created
output "eventbridge_lambda_target_id" {
  value = length(aws_cloudwatch_event_target.lambda_target) > 0 ? aws_cloudwatch_event_target.lambda_target[0].target_id : "No Lambda target created"
  description = "The ID of the EventBridge target for the Lambda function."
}
