<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |
| <a name="provider_template"></a> [template](#provider\_template) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_instance_profile.db_profile](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_instance_profile) | resource |
| [aws_iam_role.db_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_instance.db](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance) | resource |
| [aws_security_group.database_sg](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_ssm_association.database](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_association) | resource |
| [aws_ssm_document.ssm_neo4j_boostrap](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_document) | resource |
| [aws_iam_instance_profile.profile](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_instance_profile) | data source |
| [aws_iam_policy.ssm_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy) | data source |
| [aws_iam_policy_document.sts_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_security_group.sg](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/security_group) | data source |
| [aws_ssm_document.ssm](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ssm_document) | data source |
| [aws_ssm_parameter.amz_linux](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ssm_parameter) | data source |
| [aws_ssm_parameter.sshkey](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ssm_parameter) | data source |
| [template_cloudinit_config.user_data](https://registry.terraform.io/providers/hashicorp/template/latest/docs/data-sources/cloudinit_config) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_create_bootstrap_script"></a> [create\_bootstrap\_script](#input\_create\_bootstrap\_script) | choose to create bootstrap script or not | `bool` | `true` | no |
| <a name="input_create_instance_profile"></a> [create\_instance\_profile](#input\_create\_instance\_profile) | create instance profile or not | `bool` | `true` | no |
| <a name="input_create_security_group"></a> [create\_security\_group](#input\_create\_security\_group) | create security group or not | `bool` | `true` | no |
| <a name="input_database_instance_type"></a> [database\_instance\_type](#input\_database\_instance\_type) | ec2 instance type to use | `string` | `"t3.medium"` | no |
| <a name="input_database_name"></a> [database\_name](#input\_database\_name) | name of the database | `string` | `"neo4j"` | no |
| <a name="input_database_password"></a> [database\_password](#input\_database\_password) | set database password | `string` | `"custodian"` | no |
| <a name="input_db_boostrap_ssm_document"></a> [db\_boostrap\_ssm\_document](#input\_db\_boostrap\_ssm\_document) | ssm document for db boostrap | `string` | `null` | no |
| <a name="input_db_iam_profile_name"></a> [db\_iam\_profile\_name](#input\_db\_iam\_profile\_name) | name of iam profile to apply | `string` | `null` | no |
| <a name="input_db_instance_volume_size"></a> [db\_instance\_volume\_size](#input\_db\_instance\_volume\_size) | volume size of the instances | `number` | `100` | no |
| <a name="input_db_private_ip"></a> [db\_private\_ip](#input\_db\_private\_ip) | private ip of the db instance | `string` | n/a | yes |
| <a name="input_db_security_group_name"></a> [db\_security\_group\_name](#input\_db\_security\_group\_name) | provide existing security group | `string` | `null` | no |
| <a name="input_db_subnet_id"></a> [db\_subnet\_id](#input\_db\_subnet\_id) | subnet id to launch db | `string` | n/a | yes |
| <a name="input_ebs_volume_type"></a> [ebs\_volume\_type](#input\_ebs\_volume\_type) | EVS volume type | `string` | `"standard"` | no |
| <a name="input_enable_http_endpoint"></a> [enable\_http\_endpoint](#input\_enable\_http\_endpoint) | choose if http\_endpoint is enabled or disabld | `string` | `"enabled"` | no |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_public_ssh_key_ssm_parameter_name"></a> [public\_ssh\_key\_ssm\_parameter\_name](#input\_public\_ssh\_key\_ssm\_parameter\_name) | name of the ssm parameter holding ssh key content | `string` | `"ssh_public_key"` | no |
| <a name="input_require_http_tokens"></a> [require\_http\_tokens](#input\_require\_http\_tokens) | choose if http\_tokens is required or optional | `string` | `"optional"` | no |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | the prefix to add when creating resources | `string` | n/a | yes |
| <a name="input_ssh_key_name"></a> [ssh\_key\_name](#input\_ssh\_key\_name) | name of the ssh key to manage the instances | `string` | `"devops"` | no |
| <a name="input_ssh_user"></a> [ssh\_user](#input\_ssh\_user) | name of the ec2 user | `string` | `"bento"` | no |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | vpc id to to launch the ALB | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_db_security_group_arn"></a> [db\_security\_group\_arn](#output\_db\_security\_group\_arn) | n/a |
| <a name="output_db_security_group_id"></a> [db\_security\_group\_id](#output\_db\_security\_group\_id) | n/a |
| <a name="output_private_ip"></a> [private\_ip](#output\_private\_ip) | n/a |
<!-- END_TF_DOCS -->