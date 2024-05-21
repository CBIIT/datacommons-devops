resource "aws_cloudwatch_event_rule" "module_event" {
  name                = var.eventbridge_name
  schedule_expression = var.schedule_expression
  role_arn            = aws_iam_role.eventbridge_role.arn
}



# For ECS Task
resource "aws_cloudwatch_event_target" "ecs_target" {
  count = local.ecs_conditions ? 1 : 0

  rule      = aws_cloudwatch_event_rule.module_event.name
  arn       = var.target_arn
  target_id = "${var.target_type}-${aws_cloudwatch_event_rule.module_event.name}"
  role_arn  = var.role_arn
  ecs_target {
    task_definition_arn = var.task_definition_arn
    task_count          = 1
    launch_type         = "FARGATE"
    network_configuration {
      subnets         = var.private_subnet_ids
      security_groups = var.ecs_security_groups
      assign_public_ip = var.assign_public_ip
    }
  }
  // Log failed invocations
  cloudwatch_logs {
    log_group_name  = aws_cloudwatch_log_group.eventbridge_log_group.name
    log_stream_name = aws_cloudwatch_log_stream.eventbridge_log_stream.name
  }
}

# For Lambda Function
resource "aws_cloudwatch_event_target" "lambda_target" {
  count = local.lambda_conditions ? 1 : 0

  rule      = aws_cloudwatch_event_rule.module_event.name
  arn       = var.target_arn
  target_id = "${var.target_type}-${aws_cloudwatch_event_rule.module_event.name}"
  role_arn            = aws_iam_role.eventbridge_role.arn

}
