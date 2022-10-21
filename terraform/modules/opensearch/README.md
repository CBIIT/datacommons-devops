## Notes on module configuration:

- Project decides if a service-linked role is created by the module. 
- HTTPS is enforced using TLS 1.2 by default for security purposes. 
- Encryption is applied at rest by default for security purposes.
- Node-to-node encryption is applied by default for security purposes.
- A security group is created by the module - but the project must specify the security group rules to attach to the security group. The security group identifiers are exported as outputs to use as a reference in rule development at the project level.
- Automated snapshots are on by default
- Auto-tune is enabled by default, but can be disabled at by passing in "DISABLED" from the project for the opensearch_autotune_desired_state argument. Autotune set to occur daily at 11:59 PM EST. 
- Logs are sent to cloudwatch, and cloudwatch group created in module. Need to decide as team as to which logs to send from OpenSearch.



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
| [aws_cloudwatch_log_group.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_resource_policy.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_resource_policy) | resource |
| [aws_iam_service_linked_role.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_service_linked_role) | resource |
| [aws_opensearch_domain.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearch_domain) | resource |
| [aws_security_group.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_caller_identity.caller](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.region](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_automated_snapshot_start_hour"></a> [automated\_snapshot\_start\_hour](#input\_automated\_snapshot\_start\_hour) | hour when automated snapshot to be taken | `number` | `23` | no |
| <a name="input_create_cloudwatch_log_policy"></a> [create\_cloudwatch\_log\_policy](#input\_create\_cloudwatch\_log\_policy) | Due cloudwatch log policy limits, this should be option, we can use an existing policy | `bool` | `false` | no |
| <a name="input_create_os_service_role"></a> [create\_os\_service\_role](#input\_create\_os\_service\_role) | change this value to true if running this script for the first time | `bool` | `false` | no |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_multi_az_enabled"></a> [multi\_az\_enabled](#input\_multi\_az\_enabled) | set to true to enable multi-az deployment | `bool` | n/a | yes |
| <a name="input_opensearch_autotune_rollback_type"></a> [opensearch\_autotune\_rollback\_type](#input\_opensearch\_autotune\_rollback\_type) | Tell OpenSearch how to respond to disabling AutoTune. Options include NO\_ROLLBACK and DEFAULT\_ROLLBACK | `string` | `"DEFAULT_ROLLBACK"` | no |
| <a name="input_opensearch_autotune_state"></a> [opensearch\_autotune\_state](#input\_opensearch\_autotune\_state) | Tell OpenSearch to enable or disable autotuning. Options include ENABLED and DISABLED | `string` | `"ENABLED"` | no |
| <a name="input_opensearch_ebs_volume_size"></a> [opensearch\_ebs\_volume\_size](#input\_opensearch\_ebs\_volume\_size) | size of the ebs volume attached to the opensearch instance | `number` | `30` | no |
| <a name="input_opensearch_instance_count"></a> [opensearch\_instance\_count](#input\_opensearch\_instance\_count) | the number of data nodes to provision for each instance in the cluster | `number` | `2` | no |
| <a name="input_opensearch_instance_type"></a> [opensearch\_instance\_type](#input\_opensearch\_instance\_type) | type of instance to be used to create the OpenSearch cluster | `string` | `"t3.medium.search"` | no |
| <a name="input_opensearch_log_types"></a> [opensearch\_log\_types](#input\_opensearch\_log\_types) | List of log types that OpenSearch forwards to CloudWatch. Options include INDEX\_SLOW\_LOGS, SEARCH\_SLOW\_LOGS, ES\_APPLICATION\_LOGS, AUDIT\_LOGS | `list(string)` | <pre>[<br>  "AUDIT_LOGS"<br>]</pre> | no |
| <a name="input_opensearch_subnet_ids"></a> [opensearch\_subnet\_ids](#input\_opensearch\_subnet\_ids) | list of subnet ids to use | `list(string)` | n/a | yes |
| <a name="input_opensearch_tls_policy"></a> [opensearch\_tls\_policy](#input\_opensearch\_tls\_policy) | Provide the TLS policy to associate with the OpenSearch domain to enforce HTTPS communications | `string` | `"Policy-Min-TLS-1-2-2019-07"` | no |
| <a name="input_opensearch_version"></a> [opensearch\_version](#input\_opensearch\_version) | specify es version | `string` | `"OpenSearch_1.2"` | no |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | the ID of the VPC the OpenSearch cluster is being deployed into | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_opensearch_arn"></a> [opensearch\_arn](#output\_opensearch\_arn) | the OpenSearch domain arn |
| <a name="output_opensearch_cloudwatch_log_group_arn"></a> [opensearch\_cloudwatch\_log\_group\_arn](#output\_opensearch\_cloudwatch\_log\_group\_arn) | the log group arn that collects OpenSearch logs |
| <a name="output_opensearch_endpoint"></a> [opensearch\_endpoint](#output\_opensearch\_endpoint) | the opensearch domain endpoint url |
| <a name="output_opensearch_security_group_arn"></a> [opensearch\_security\_group\_arn](#output\_opensearch\_security\_group\_arn) | the arn of the security group associated with the OpenSearch cluster |
| <a name="output_opensearch_security_group_id"></a> [opensearch\_security\_group\_id](#output\_opensearch\_security\_group\_id) | the id of the security group associated with the OpenSearch cluster |
<!-- END_TF_DOCS -->