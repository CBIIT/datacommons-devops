locals {
  ecs_conditions    = var.target_type == "ecs-task"
  lambda_conditions = var.target_type == "lambda"
}
