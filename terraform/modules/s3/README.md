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
| [aws_s3_bucket.s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_acl.s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_acl) | resource |
| [aws_s3_bucket_intelligent_tiering_configuration.s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_intelligent_tiering_configuration) | resource |
| [aws_s3_bucket_logging.s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_logging) | resource |
| [aws_s3_bucket_public_access_block.s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [aws_s3_bucket_versioning.s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_versioning) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_bucket_name"></a> [bucket\_name](#input\_bucket\_name) | name of the s3 bucket | `string` | n/a | yes |
| <a name="input_days_for_archive_tiering"></a> [days\_for\_archive\_tiering](#input\_days\_for\_archive\_tiering) | Number of days of consecutive lack of access for an object before it is archived | `number` | n/a | yes |
| <a name="input_days_for_deep_archive_tiering"></a> [days\_for\_deep\_archive\_tiering](#input\_days\_for\_deep\_archive\_tiering) | Number of days of consecutive lack of access for an object before it is archived deeply | `number` | n/a | yes |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_s3_access_log_bucket_id"></a> [s3\_access\_log\_bucket\_id](#input\_s3\_access\_log\_bucket\_id) | The destination bucket of access logs for an S3 bucket | `string` | n/a | yes |
| <a name="input_s3_bucket_policy"></a> [s3\_bucket\_policy](#input\_s3\_bucket\_policy) | This optional s3 bucket policy | `string` | `null` | no |
| <a name="input_s3_enable_access_logging"></a> [s3\_enable\_access\_logging](#input\_s3\_enable\_access\_logging) | set to true to enable s3 access logging | `bool` | `true` | no |
| <a name="input_s3_force_destroy"></a> [s3\_force\_destroy](#input\_s3\_force\_destroy) | force destroy s3 bucket | `string` | n/a | yes |
| <a name="input_s3_intelligent_tiering_status"></a> [s3\_intelligent\_tiering\_status](#input\_s3\_intelligent\_tiering\_status) | Set the status of the intelligent tiering configuration. Options include Enabled and Disabled | `string` | `"Enabled"` | no |
| <a name="input_s3_log_prefix"></a> [s3\_log\_prefix](#input\_s3\_log\_prefix) | The prefix for the destination of the server access logs for an S3 bucket | `string` | `"logs/"` | no |
| <a name="input_s3_versioning_status"></a> [s3\_versioning\_status](#input\_s3\_versioning\_status) | Set the status of the bucket versioning feature. Options include Enabled and Disabled | `string` | `"Enabled"` | no |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this resource | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_bucket_id"></a> [bucket\_id](#output\_bucket\_id) | bucket id |
| <a name="output_bucket_name"></a> [bucket\_name](#output\_bucket\_name) | name of the bucket |
<!-- END_TF_DOCS -->