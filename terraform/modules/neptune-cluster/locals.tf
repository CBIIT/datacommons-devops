locals {
  create_parameter_groups = var.enable_serverless ? false : var.create_parameter_groups
}
