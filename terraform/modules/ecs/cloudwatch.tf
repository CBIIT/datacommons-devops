resource "aws_cloudwatch_log_group" "ecs_execute_command_log_group" {
  name              = local.ecs_exec_log_group
  retention_in_days = 90
}