locals {
  permission_boundary_arn = var.level == "prod" ? null : "arn:aws:iam::${var.account_id}:policy/PermissionBoundary_PowerUser"
}