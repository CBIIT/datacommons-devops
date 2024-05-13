resource "aws_cloudwatch_event_rule" "module_event" {
  name                = var.eventbridge_name
  schedule_expression = var.schedule_expression
}

# For ECS Task
resource "aws_cloudwatch_event_target" "ecs_target" {
  count = local.ecs_conditions ? 1 : 0

  rule      = aws_cloudwatch_event_rule.module_event.name
  arn       = var.target_arn
  target_id = "${var.target_type}-${aws_cloudwatch_event_rule.module_event.name}"
  
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
}

# For Lambda Function
resource "aws_cloudwatch_event_target" "lambda_target" {
  count = local.lambda_conditions ? 1 : 0

  rule      = aws_cloudwatch_event_rule.module_event.name
  arn       = var.target_arn
  target_id = "${var.target_type}-${aws_cloudwatch_event_rule.module_event.name}"

  lambda_target {
    function_arn = var.target_arn
  }
}
