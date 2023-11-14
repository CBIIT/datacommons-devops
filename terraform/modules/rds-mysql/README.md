![Frederick National Laboratory](./assets/fnl.svg)

# Overview

# Usage

<!-- BEGIN_TF_DOCS -->
# Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.0 |

# Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | >= 4.0 |

# Resources

| Name | Type |
|------|------|
| [aws_db_instance.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance) | resource |
| [aws_db_subnet_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_subnet_group) | resource |
| [aws_iam_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_security_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_security_group_rule.inbound](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group_rule) | resource |
| [aws_security_group_rule.outbound](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group_rule) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.trust](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

# Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allocated_storage"></a> [allocated\_storage](#input\_allocated\_storage) | allocated storage in gibibytes - minimum is 100 | `number` | `100` | no |
| <a name="input_allow_major_version_upgrade"></a> [allow\_major\_version\_upgrade](#input\_allow\_major\_version\_upgrade) | allow major version upgrade | `bool` | `false` | no |
| <a name="input_app"></a> [app](#input\_app) | the name of the application expressed as an acronym | `string` | n/a | yes |
| <a name="input_apply_immediately"></a> [apply\_immediately](#input\_apply\_immediately) | whether to apply changes immediately or wait until next maintenance window | `bool` | `true` | no |
| <a name="input_attach_permissions_boundary"></a> [attach\_permissions\_boundary](#input\_attach\_permissions\_boundary) | whether to attach a permissions boundary to the role - required if enable\_enhanced\_monitoring is true | `bool` | `null` | no |
| <a name="input_auto_minor_version_upgrade"></a> [auto\_minor\_version\_upgrade](#input\_auto\_minor\_version\_upgrade) | whether minor database modifications are automatically applied during maintenance windows | `bool` | `true` | no |
| <a name="input_backup_retention_period"></a> [backup\_retention\_period](#input\_backup\_retention\_period) | backup retention period in days - between 0 and 35 | `number` | `7` | no |
| <a name="input_backup_window"></a> [backup\_window](#input\_backup\_window) | backup window in UTC - format hh24:mi-hh24:mi | `string` | `"02:00-04:00"` | no |
| <a name="input_create_db_subnet_group"></a> [create\_db\_subnet\_group](#input\_create\_db\_subnet\_group) | whether to create a db subnet group | `bool` | `true` | no |
| <a name="input_create_from_snapshot"></a> [create\_from\_snapshot](#input\_create\_from\_snapshot) | whether to create the instance from a snapshot - if true, provide shapshot id for snapshot\_identifier variable | `bool` | `false` | no |
| <a name="input_create_security_group"></a> [create\_security\_group](#input\_create\_security\_group) | Whether to create a security group for the rds instance | `bool` | `true` | no |
| <a name="input_db_name"></a> [db\_name](#input\_db\_name) | name of the database within RDS to create | `string` | n/a | yes |
| <a name="input_db_subnet_group_name"></a> [db\_subnet\_group\_name](#input\_db\_subnet\_group\_name) | name of the db subnet group - required if create\_db\_subnet\_group is false | `string` | `null` | no |
| <a name="input_deletion_protection"></a> [deletion\_protection](#input\_deletion\_protection) | whether to enable deletion protection | `bool` | `true` | no |
| <a name="input_enable_enhanced_monitoring"></a> [enable\_enhanced\_monitoring](#input\_enable\_enhanced\_monitoring) | whether to enable enhanced monitoring | `bool` | `true` | no |
| <a name="input_enabled_cloudwatch_logs_exports"></a> [enabled\_cloudwatch\_logs\_exports](#input\_enabled\_cloudwatch\_logs\_exports) | list of log types to export to cloudwatch | `list(string)` | <pre>[<br>  "audit",<br>  "error",<br>  "general",<br>  "slowquery"<br>]</pre> | no |
| <a name="input_engine"></a> [engine](#input\_engine) | database engine to use | `string` | `"mysql"` | no |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | database engine version to use - if auto\_minor\_version\_upgrade is true, no need to specify patch version | `string` | `"8.0"` | no |
| <a name="input_env"></a> [env](#input\_env) | the target tier ('dev', 'qa', 'stage', 'nonprod' or 'prod'.) | `string` | n/a | yes |
| <a name="input_iam_database_authentication_enabled"></a> [iam\_database\_authentication\_enabled](#input\_iam\_database\_authentication\_enabled) | whether to enable iam database authentication | `bool` | `false` | no |
| <a name="input_instance_class"></a> [instance\_class](#input\_instance\_class) | rds instance class to use | `string` | `"db.t3.medium"` | no |
| <a name="input_iops"></a> [iops](#input\_iops) | iops to associate with the instance - only valid for 'io1' and 'gp3' storage types | `number` | `3000` | no |
| <a name="input_maintenance_window"></a> [maintenance\_window](#input\_maintenance\_window) | maintenance window in UTC - format ddd:hh24:mi-ddd:hh24:mi | `string` | `"sun:20:00-sun:23:00"` | no |
| <a name="input_monitoring_interval"></a> [monitoring\_interval](#input\_monitoring\_interval) | interval in seconds to monitor the instance - 0 to disable, otherwise 1, 5, 10, 15, 30 , and 60 are valid | `number` | `10` | no |
| <a name="input_multi_az"></a> [multi\_az](#input\_multi\_az) | whether to create a multi-az instance | `bool` | `true` | no |
| <a name="input_password"></a> [password](#input\_password) | password for the database | `string` | n/a | yes |
| <a name="input_performance_insights_enabled"></a> [performance\_insights\_enabled](#input\_performance\_insights\_enabled) | whether to enable performance insights | `bool` | `true` | no |
| <a name="input_performance_insights_retention_period"></a> [performance\_insights\_retention\_period](#input\_performance\_insights\_retention\_period) | performance insights retention period in days - between 7 and 731 with a multiple of 31 | `number` | `7` | no |
| <a name="input_program"></a> [program](#input\_program) | the program associated with the application | `string` | n/a | yes |
| <a name="input_rds_suffix"></a> [rds\_suffix](#input\_rds\_suffix) | suffix to append to the rds instance name | `string` | `"rds"` | no |
| <a name="input_snapshot_identifier"></a> [snapshot\_identifier](#input\_snapshot\_identifier) | snapshot identifier to use for the instance - required if create\_from\_snapshot is true | `string` | `null` | no |
| <a name="input_storage_throughput"></a> [storage\_throughput](#input\_storage\_throughput) | storage throughput in gibibytes per second - only valid for 'gp3' storage type | `number` | `125` | no |
| <a name="input_storage_type"></a> [storage\_type](#input\_storage\_type) | type of ebs block storage to associate with the instance - either 'standard', 'gp2', 'gp3', or 'io1' | `string` | `"gp3"` | no |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | list of subnet ids to place the instance in - required if create\_db\_subnet\_group is true | `list(string)` | `[]` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | map of tags to apply to the instance | `map(string)` | `{}` | no |
| <a name="input_username"></a> [username](#input\_username) | username for the database | `string` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | id of the vpc to create the security group in - required if create\_security\_group is true | `string` | `null` | no |
| <a name="input_vpc_security_group_ids"></a> [vpc\_security\_group\_ids](#input\_vpc\_security\_group\_ids) | list of security group ids to associate with the instance - required if create\_security\_group is false | `list(string)` | `[]` | no |

# Outputs

| Name | Description |
|------|-------------|
| <a name="output_address"></a> [address](#output\_address) | address of the instance |
| <a name="output_arn"></a> [arn](#output\_arn) | arn of the instance |
| <a name="output_availability_zone"></a> [availability\_zone](#output\_availability\_zone) | availability zone of the instance |
| <a name="output_db_name"></a> [db\_name](#output\_db\_name) | name of the database |
| <a name="output_db_subnet_group_name"></a> [db\_subnet\_group\_name](#output\_db\_subnet\_group\_name) | name of the subnet group |
| <a name="output_domain"></a> [domain](#output\_domain) | domain of the instance |
| <a name="output_endpoint"></a> [endpoint](#output\_endpoint) | endpoint of the instance |
| <a name="output_hosted_zone_id"></a> [hosted\_zone\_id](#output\_hosted\_zone\_id) | hosted zone id of the instance |
| <a name="output_id"></a> [id](#output\_id) | id of the instance |
| <a name="output_identifier"></a> [identifier](#output\_identifier) | identifier of the instance |
| <a name="output_identifier_prefix"></a> [identifier\_prefix](#output\_identifier\_prefix) | identifier prefix of the instance |
| <a name="output_monitoring_role_arn"></a> [monitoring\_role\_arn](#output\_monitoring\_role\_arn) | monitoring role arn of the instance |
| <a name="output_password"></a> [password](#output\_password) | password of the instance |
| <a name="output_port"></a> [port](#output\_port) | port of the instance |
| <a name="output_resource_id"></a> [resource\_id](#output\_resource\_id) | resource id of the instance |
| <a name="output_security_group_arn"></a> [security\_group\_arn](#output\_security\_group\_arn) | arn of the security group - if create\_security\_group is true |
| <a name="output_security_group_id"></a> [security\_group\_id](#output\_security\_group\_id) | id of the security group - if create\_security\_group is true |
| <a name="output_security_group_name"></a> [security\_group\_name](#output\_security\_group\_name) | name of the security group - if create\_security\_group is true |
| <a name="output_username"></a> [username](#output\_username) | username of the instance |
<!-- END_TF_DOCS -->