<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_iam_assumable_role"></a> [iam\_assumable\_role](#module\_iam\_assumable\_role) | terraform-aws-modules/iam/aws//modules/iam-assumable-role | n/a |
| <a name="module_iam_policy"></a> [iam\_policy](#module\_iam\_policy) | terraform-aws-modules/iam/aws//modules/iam-policy | 5.1.0 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_add_custom_policy"></a> [add\_custom\_policy](#input\_add\_custom\_policy) | add policies other than managed policy | `bool` | `false` | no |
| <a name="input_create_role"></a> [create\_role](#input\_create\_role) | create iam role or not | `bool` | `true` | no |
| <a name="input_custom_policy_name"></a> [custom\_policy\_name](#input\_custom\_policy\_name) | name of custom policy | `string` | n/a | yes |
| <a name="input_custom_role_policy_arns"></a> [custom\_role\_policy\_arns](#input\_custom\_role\_policy\_arns) | list of policy arns defined for this role | `list(string)` | `[]` | no |
| <a name="input_iam_policy"></a> [iam\_policy](#input\_iam\_policy) | iam policy document | `string` | `null` | no |
| <a name="input_iam_policy_description"></a> [iam\_policy\_description](#input\_iam\_policy\_description) | description of iam policy | `string` | `null` | no |
| <a name="input_iam_role_name"></a> [iam\_role\_name](#input\_iam\_role\_name) | name of the role | `string` | n/a | yes |
| <a name="input_role_description"></a> [role\_description](#input\_role\_description) | description of the role | `string` | `"iam role"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | resource tags | `map(string)` | `null` | no |
| <a name="input_trusted_role_arns"></a> [trusted\_role\_arns](#input\_trusted\_role\_arns) | list of trusted roles arns | `list(string)` | `[]` | no |
| <a name="input_trusted_role_services"></a> [trusted\_role\_services](#input\_trusted\_role\_services) | list of trusted service | `list(string)` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_iam_role_arn"></a> [iam\_role\_arn](#output\_iam\_role\_arn) | n/a |
| <a name="output_iam_role_name"></a> [iam\_role\_name](#output\_iam\_role\_name) | n/a |
<!-- END_TF_DOCS -->