locals {
  kms_description          = "The AWS Key Management Service key that encrypts the data between the local client and the container."
  ecs_exec_log_group       = "${var.stack_name}-${var.env}-ecs-execute-command-logs"
  task_execution_role_name = "${var.stack_name}-${var.env}-ecs-task-execution-role"
  task_role_name           = "${var.stack_name}-${var.env}-ecs-task-role"
  task_role_policy_exec_name = "${var.stack_name}-${var.env}-ecs-task-role-exec-policy"
}