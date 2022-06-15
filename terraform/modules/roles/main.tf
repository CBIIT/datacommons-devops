module "iam_assumable_role" {
  source                            = "terraform-aws-modules/iam/aws//modules/iam-assumable-role"
  trusted_role_arns                 = var.trusted_role_arns
  create_role                       = var.create_role
  role_name                         = var.iam_role_name
  role_requires_mfa                 = false
  custom_role_policy_arns           = local.all_custom_policy_arns
  number_of_custom_role_policy_arns = length(local.all_custom_policy_arns)
  trusted_role_services             = var.trusted_role_services
  role_description                  = var.role_description
  tags                              = var.tags
}

module "iam_policy" {
  count       = var.add_custom_policy ? 1 : 0
  source      = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version     = "5.1.0"
  name        = var.custom_policy_name
  description = var.iam_policy_description
  policy      = var.iam_policy
  tags        = var.tags
}