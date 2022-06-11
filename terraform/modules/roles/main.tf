locals {
  all_custom_policy_arns = var.add_custom_policy ? concat([ module.iam_policy[0].arn],var.custom_role_policy_arns) : var.custom_role_policy_arns
}

module "iam_assumable_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role"
  version = "~> 4"
  trusted_role_arns = var.trusted_role_arns
  create_role = true
  role_name  = var.iam_role_name
  role_requires_mfa = false
  custom_role_policy_arns = local.all_custom_policy_arns
  number_of_custom_role_policy_arns = length(local.all_custom_policy_arns)
  trusted_role_services = var.trusted_role_services
}

module "iam_policy" {
  count = var.add_custom_policy ? 1 : 0
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "~> 4"
  name        =  var.custom_policy_name
  path        = "/"
  description = var.iam_policy_description
  policy = var.iam_policy
}
