data "aws_caller_identity" "current" {}

data "aws_ecs_task_definition" "latest" {
  family = var.task_family
}
