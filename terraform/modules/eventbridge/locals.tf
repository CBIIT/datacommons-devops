locals {
  ecs_conditions    = var.target_type == "ecs-task"
  lambda_conditions = var.target_type == "lambda"
  permission_boundary_arn  = terraform.workspace == "stage" || terraform.workspace == "prod" ? null : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
}
