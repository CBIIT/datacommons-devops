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
| [aws_kms_alias.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_alias) | resource |
| [aws_kms_key.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key) | resource |
| [aws_kms_key_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key_policy) | resource |
| [aws_neptune_cluster.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/neptune_cluster) | resource |
| [aws_neptune_cluster_instance.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/neptune_cluster_instance) | resource |
| [aws_neptune_cluster_parameter_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/neptune_cluster_parameter_group) | resource |
| [aws_neptune_parameter_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/neptune_parameter_group) | resource |
| [aws_neptune_subnet_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/neptune_subnet_group) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.kms](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allow_major_version_upgrade"></a> [allow\_major\_version\_upgrade](#input\_allow\_major\_version\_upgrade) | indicates that major version upgrades are allowed | `string` | `false` | no |
| <a name="input_apply_immediately"></a> [apply\_immediately](#input\_apply\_immediately) | indicates whether the changes should be applied immediately or during the next maintenance window | `string` | `true` | no |
| <a name="input_auto_minor_version_upgrade"></a> [auto\_minor\_version\_upgrade](#input\_auto\_minor\_version\_upgrade) | indicates that minor engine upgrades are applied automatically to the instance during the maintenance window | `bool` | `true` | no |
| <a name="input_backup_retention_period"></a> [backup\_retention\_period](#input\_backup\_retention\_period) | number of days to retain backups for | `string` | `1` | no |
| <a name="input_copy_tags_to_snapshot"></a> [copy\_tags\_to\_snapshot](#input\_copy\_tags\_to\_snapshot) | whether to copy tags to snapshots | `bool` | `true` | no |
| <a name="input_create_kms_key"></a> [create\_kms\_key](#input\_create\_kms\_key) | whether to create the kms key that encrypts the cluster and instance(s) | `bool` | `true` | no |
| <a name="input_create_parameter_groups"></a> [create\_parameter\_groups](#input\_create\_parameter\_groups) | whether to create parameter groups for the cluster and instance(s) | `bool` | `false` | no |
| <a name="input_database_subnet_ids"></a> [database\_subnet\_ids](#input\_database\_subnet\_ids) | the list of subnet IDs to associate with the cluster | `set(string)` | n/a | yes |
| <a name="input_deletion_protection"></a> [deletion\_protection](#input\_deletion\_protection) | whether to enable deletion protection | `bool` | `true` | no |
| <a name="input_enable_audit_log"></a> [enable\_audit\_log](#input\_enable\_audit\_log) | whether to enable audit logs at the cluster level | `bool` | `true` | no |
| <a name="input_enable_caching"></a> [enable\_caching](#input\_enable\_caching) | whether to enable caching for the cluster | `bool` | `false` | no |
| <a name="input_enable_cloudwatch_logs_exports"></a> [enable\_cloudwatch\_logs\_exports](#input\_enable\_cloudwatch\_logs\_exports) | list of log types to export to cloudwatch | `list(string)` | <pre>[<br>  "audit"<br>]</pre> | no |
| <a name="input_enable_result_cache"></a> [enable\_result\_cache](#input\_enable\_result\_cache) | whether to enable the result cache for the instances in the cluster | `bool` | `false` | no |
| <a name="input_enable_serverless"></a> [enable\_serverless](#input\_enable\_serverless) | whether to enable serverless mode for the cluster | `bool` | `true` | no |
| <a name="input_enable_slow_query_log"></a> [enable\_slow\_query\_log](#input\_enable\_slow\_query\_log) | the log level for slow queries applied at the cluster-level - either 'info', 'debug', or 'disable' | `string` | `"info"` | no |
| <a name="input_engine"></a> [engine](#input\_engine) | the name of the database engine to be used for this instance | `string` | `"neptune"` | no |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | the version of the database engine to use | `string` | `"1.3.1.0"` | no |
| <a name="input_final_snapshot_identifier"></a> [final\_snapshot\_identifier](#input\_final\_snapshot\_identifier) | the name of the final snapshot to be created immediately before deleting the cluster | `string` | `null` | no |
| <a name="input_iam_database_authentication_enabled"></a> [iam\_database\_authentication\_enabled](#input\_iam\_database\_authentication\_enabled) | whether to enable IAM database authentication for the cluster | `bool` | `false` | no |
| <a name="input_iam_roles"></a> [iam\_roles](#input\_iam\_roles) | the list of IAM roles to associate with the cluster | `set(string)` | `[]` | no |
| <a name="input_instance_class"></a> [instance\_class](#input\_instance\_class) | the instance class to use (i.e., db.r5.large) - only required when serverless is not enabled | `string` | `"db.r5.large"` | no |
| <a name="input_max_capacity"></a> [max\_capacity](#input\_max\_capacity) | the maximum capacity for the cluster in neptune capacity units when serverless is enabled | `number` | `128` | no |
| <a name="input_min_capacity"></a> [min\_capacity](#input\_min\_capacity) | the minimum capacity for the cluster in neptune capacity units when serverless is enabled | `number` | `2` | no |
| <a name="input_parameter_group_family"></a> [parameter\_group\_family](#input\_parameter\_group\_family) | the family of the neptune cluster parameter group (i.e. neptune1.3) | `string` | `"neptune1.3"` | no |
| <a name="input_port"></a> [port](#input\_port) | the port on which the DB accepts connections | `number` | `8182` | no |
| <a name="input_preferred_backup_window"></a> [preferred\_backup\_window](#input\_preferred\_backup\_window) | the daily time range during which automated backups are created if automated backups are enabled | `string` | `"02:00-04:00"` | no |
| <a name="input_preferred_maintenance_window"></a> [preferred\_maintenance\_window](#input\_preferred\_maintenance\_window) | the weekly time range during which system maintenance can occur, in (UTC) | `string` | `"sun:05:00-sun:09:00"` | no |
| <a name="input_query_timeout"></a> [query\_timeout](#input\_query\_timeout) | time in milliseconds that a query can run before it is terminated by the cluster | `string` | `"60000"` | no |
| <a name="input_replication_source_identifier"></a> [replication\_source\_identifier](#input\_replication\_source\_identifier) | the ARN of the source Neptune instance if this Neptune instance is a read replica | `string` | `null` | no |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | the prefix to add when creating resources | `string` | n/a | yes |
| <a name="input_skip_final_snapshot"></a> [skip\_final\_snapshot](#input\_skip\_final\_snapshot) | whether to skip the creation of a final snapshot before deleting the cluster | `bool` | `true` | no |
| <a name="input_slow_query_log_threshold"></a> [slow\_query\_log\_threshold](#input\_slow\_query\_log\_threshold) | the threshold in milliseconds for slow queries applied at the cluster level | `number` | `5000` | no |
| <a name="input_snapshot_identifier"></a> [snapshot\_identifier](#input\_snapshot\_identifier) | the name of an existing snapshot from which to create this cluster | `string` | `null` | no |
| <a name="input_vpc_security_group_ids"></a> [vpc\_security\_group\_ids](#input\_vpc\_security\_group\_ids) | the list of security group IDs to associate with the cluster | `set(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_cluster_arn"></a> [cluster\_arn](#output\_cluster\_arn) | the neptune cluster arn |
| <a name="output_cluster_endpoint"></a> [cluster\_endpoint](#output\_cluster\_endpoint) | the neptune cluster endpoint |
| <a name="output_cluster_id"></a> [cluster\_id](#output\_cluster\_id) | the neptune cluster id |
| <a name="output_cluster_identifier"></a> [cluster\_identifier](#output\_cluster\_identifier) | the neptune cluster identifier |
| <a name="output_cluster_members"></a> [cluster\_members](#output\_cluster\_members) | the neptune cluster members |
| <a name="output_cluster_port"></a> [cluster\_port](#output\_cluster\_port) | the neptune cluster port |
| <a name="output_cluster_reader_endpoint"></a> [cluster\_reader\_endpoint](#output\_cluster\_reader\_endpoint) | the neptune cluster reader endpoint |
| <a name="output_cluster_resource_id"></a> [cluster\_resource\_id](#output\_cluster\_resource\_id) | the neptune cluster resource id |
| <a name="output_instance_address"></a> [instance\_address](#output\_instance\_address) | The hostname of the instance. See also endpoint and port. |
| <a name="output_instance_arn"></a> [instance\_arn](#output\_instance\_arn) | The ARN of the neptune instance |
| <a name="output_instance_cluster_identifier"></a> [instance\_cluster\_identifier](#output\_instance\_cluster\_identifier) | The neptune cluster identifier |
| <a name="output_instance_dbi_resource_id"></a> [instance\_dbi\_resource\_id](#output\_instance\_dbi\_resource\_id) | The neptune instance resource ID |
| <a name="output_instance_endpoint"></a> [instance\_endpoint](#output\_instance\_endpoint) | The hostname of the instance. See also address and port. |
| <a name="output_instance_id"></a> [instance\_id](#output\_instance\_id) | The neptune instance ID |
| <a name="output_instance_identifier"></a> [instance\_identifier](#output\_instance\_identifier) | The neptune instance identifier |
| <a name="output_kms_alias_arn"></a> [kms\_alias\_arn](#output\_kms\_alias\_arn) | the neptune cluster kms key alias arn |
| <a name="output_kms_alias_id"></a> [kms\_alias\_id](#output\_kms\_alias\_id) | the neptune cluster kms key alias id |
| <a name="output_kms_alias_name"></a> [kms\_alias\_name](#output\_kms\_alias\_name) | the neptune cluster kms key alias name |
| <a name="output_kms_key_arn"></a> [kms\_key\_arn](#output\_kms\_key\_arn) | the neptune cluster kms key arn |
| <a name="output_kms_key_id"></a> [kms\_key\_id](#output\_kms\_key\_id) | the neptune cluster kms key id |
<!-- END_TF_DOCS -->