locals {
  all_custom_policy_arns = var.add_custom_policy ? concat([module.iam_policy[0].arn], var.custom_role_policy_arns) : var.custom_role_policy_arns
}