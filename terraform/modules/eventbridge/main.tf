resource "aws_eventbridge_rule" "module_event" {
  name                = var.name
  schedule_expression = var.schedule_expression
}

resource "aws_eventbridge_target" "module_target" {
  rule      = aws_eventbridge_rule.module_event.name
  arn       = var.target_arn
  target_id = "${var.target_type}-${aws_eventbridge_rule.module_event.name}"

  input_transformer {
    input_paths    = var.input_paths
    input_template = var.input
  }

  dynamic "ecs_parameters" {
    for_each = local.ecs_conditions ? [1] : []
    content {
      task_definition_arn = var.task_definition_arn
      task_count          = 1
      launch_type         = "FARGATE"
      network_configuration {
        ecs_subnet_ids   = var.private_subnet_ids
        security_groups   = var.security_groups
        assign_public_ip  = var.assign_public_ip
      }
    }
  }

  dynamic "lambda_parameters" {
    for_each = local.lambda_conditions ? [1] : []
    content {
      function_arn = var.target_arn
    }
  }
}
