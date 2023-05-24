locals {
  kms_description                 = "The AWS Key Management Service key that encrypts the data between the local client and the container."
  ecs_exec_log_group              = "${var.resource_prefix}-ecs-execute-command-logs"
  task_execution_role_name        = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-ecs-task-execution-role" : "${var.resource_prefix}-task-execution-role"
  task_role_name                  = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-ecs-task-role" : "${var.resource_prefix}-task-role"
  task_role_policy_exec_name      = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-ecs-task-role-exec-policy" : "${var.resource_prefix}-task-role-exec-policy"
  task_execution_role_policy_name = var.target_account_cloudone ? "${var.iam_prefix}-${var.resource_prefix}-ecs-task-execution-role-policy" : "${var.resource_prefix}-task-execution-role-policy"
  nih_cidr_ranges                 = ["129.43.0.0/16", "137.187.0.0/16", "10.128.0.0/9", "165.112.0.0/16", "156.40.0.0/16", "10.208.0.0/21", "128.231.0.0/16", "130.14.0.0/16", "157.98.0.0/16", "10.133.0.0/16"]
  vpc_cidr                        = data.aws_vpc.current.cidr_block
  permission_boundary_arn         = var.env == "prod" || var.env == "stage" ? null : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
  os_domain_name                  = var.add_opensearch_permission ? "${var.resource_prefix}-opensearch" : "*"
}