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
| [aws_ecr_lifecycle_policy.ecr_life_cycle](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_lifecycle_policy) | resource |
| [aws_ecr_registry_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_registry_policy) | resource |
| [aws_ecr_replication_configuration.replication](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_replication_configuration) | resource |
| [aws_ecr_repository.ecr](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository) | resource |
| [aws_ecr_repository_policy.ecr_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository_policy) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.ecr_policy_doc](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allow_ecr_replication"></a> [allow\_ecr\_replication](#input\_allow\_ecr\_replication) | allow ecr replication | `bool` | `false` | no |
| <a name="input_resource_prefix"></a> [create\_env\_specific\_repo](#input\_resource\_prefix) | the prefix to add when creating resources | `string` | n/a | yes |
| <a name="input_ecr_repo_names"></a> [ecr\_repo\_names](#input\_ecr\_repo\_names) | list of repo names | `list(string)` | n/a | yes |
| <a name="input_enable_ecr_replication"></a> [enable\_ecr\_replication](#input\_enable\_ecr\_replication) | enable ecr replication | `bool` | `false` | no |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_replication_destination_registry_id"></a> [replication\_destination\_registry\_id](#input\_replication\_destination\_registry\_id) | registry id for destination image | `string` | `""` | no |
| <a name="input_replication_source_registry_id"></a> [replication\_source\_registry\_id](#input\_replication\_source\_registry\_id) | registry id for source image | `string` | `""` | no |
| <a name="input_project"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->