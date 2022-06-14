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
| [aws_cloudwatch_log_group.es](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_resource_policy.es](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_resource_policy) | resource |
| [aws_iam_service_linked_role.es](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_service_linked_role) | resource |
| [aws_opensearch_domain.es](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearch_domain) | resource |
| [aws_caller_identity.caller](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_region.region](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_automated_snapshot_start_hour"></a> [automated\_snapshot\_start\_hour](#input\_automated\_snapshot\_start\_hour) | hour when automated snapshot to be taken | `number` | `23` | no |
| <a name="input_create_os_service_role"></a> [create\_os\_service\_role](#input\_create\_os\_service\_role) | change this value to true if running this script for the first time | `bool` | `false` | no |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_multi_az_enabled"></a> [multi\_az\_enabled](#input\_multi\_az\_enabled) | set to true to enable multi-az deployment | `bool` | n/a | yes |
| <a name="input_opensearch_ebs_volume_size"></a> [opensearch\_ebs\_volume\_size](#input\_opensearch\_ebs\_volume\_size) | size of the ebs volume attached to the opensearch instance | `number` | `200` | no |
| <a name="input_opensearch_instance_count"></a> [opensearch\_instance\_count](#input\_opensearch\_instance\_count) | the number of data nodes to provision for each instance in the cluster | `any` | n/a | yes |
| <a name="input_opensearch_instance_type"></a> [opensearch\_instance\_type](#input\_opensearch\_instance\_type) | type of instance to be used to create the elasticsearch cluster | `string` | `"t3.medium.elasticsearch"` | no |
| <a name="input_opensearch_log_type"></a> [opensearch\_log\_type](#input\_opensearch\_log\_type) | type of opensearch logs to send to cloudwatch (INDEX\_SLOW\_LOGS, SEARCH\_SLOW\_LOGS, AUDIT\_LOGS, ES\_APPLICATION\_LOGS) | `string` | `"INDEX_SLOW_LOGS"` | no |
| <a name="input_opensearch_logs_enabled"></a> [opensearch\_logs\_enabled](#input\_opensearch\_logs\_enabled) | set to true to enable OpenSearch to forward logs to CloudWatch | `bool` | `true` | no |
| <a name="input_opensearch_security_group_ids"></a> [opensearch\_security\_group\_ids](#input\_opensearch\_security\_group\_ids) | security group ids to apply to this resource | `list(string)` | n/a | yes |
| <a name="input_opensearch_subnet_ids"></a> [opensearch\_subnet\_ids](#input\_opensearch\_subnet\_ids) | list of subnet ids to use | `list(string)` | n/a | yes |
| <a name="input_opensearch_version"></a> [opensearch\_version](#input\_opensearch\_version) | specify es version | `string` | `"OpenSearch_1.2"` | no |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_opensearch_arn"></a> [opensearch\_arn](#output\_opensearch\_arn) | the OpenSearch domain arn |
| <a name="output_opensearch_cloudwatch_log_group_arn"></a> [opensearch\_cloudwatch\_log\_group\_arn](#output\_opensearch\_cloudwatch\_log\_group\_arn) | the log group arn that collects OpenSearch logs |
| <a name="output_opensearch_endpoint"></a> [opensearch\_endpoint](#output\_opensearch\_endpoint) | the opensearch domain endpoint url |
<!-- END_TF_DOCS -->