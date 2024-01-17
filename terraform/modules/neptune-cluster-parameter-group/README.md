<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_neptune_cluster_parameter_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/neptune_cluster_parameter_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_enable_audit_log"></a> [enable\_audit\_log](#input\_enable\_audit\_log) | whether to enable audit logs | `bool` | `true` | no |
| <a name="input_family"></a> [family](#input\_family) | the family of the neptune cluster parameter group | `string` | `"neptune1.2"` | no |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | the prefix to add when creating resources | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_arn"></a> [arn](#output\_arn) | arn of the neptune cluster parameter group |
| <a name="output_family"></a> [family](#output\_family) | family of the neptune cluster parameter group |
| <a name="output_id"></a> [id](#output\_id) | id of the neptune cluster parameter group |
| <a name="output_name"></a> [name](#output\_name) | name of the neptune cluster parameter group |
<!-- END_TF_DOCS -->