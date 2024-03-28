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
| [aws_iam_policy.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.attach](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_s3_bucket.source](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_replication_configuration.replication](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_replication_configuration) | resource |
| [aws_s3_bucket_versioning.source](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_versioning) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.source](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_s3_bucket.source](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/s3_bucket) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_create_source_bucket"></a> [create\_source\_bucket](#input\_create\_source\_bucket) | choose to create source bucket | `bool` | `false` | no |
| <a name="input_destination_bucket_name"></a> [destination\_bucket\_name](#input\_destination\_bucket\_name) | destination bucket name | `string` | `""` | no |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_iam_prefix"></a> [iam\_prefix](#input\_iam\_prefix) | The string prefix for IAM roles and policies to conform to NCI power-user compliance | `string` | `"power-user"` | no |
| <a name="input_replication_destination_account_id"></a> [replication\_destination\_account\_id](#input\_replication\_destination\_account\_id) | replication account id | `string` | `""` | no |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | The string prefix for resource names | `string` | n/a | yes |
| <a name="input_source_bucket_name"></a> [source\_bucket\_name](#input\_source\_bucket\_name) | source bucket name | `string` | `""` | no |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_target_account_cloudone"></a> [target\_account\_cloudone](#input\_target\_account\_cloudone) | to add check conditions on whether the resources are brought up in cloudone or not | `bool` | `false` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->