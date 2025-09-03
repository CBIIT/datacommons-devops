# Setting up ECS Exec
- It’s important to notice that the container image requires `script` (part of util-linux) and `cat` (part of coreutils) to be installed in order to have command logs uploaded correctly to S3 and/or CloudWatch. The nginx container images have this support already installed. 
- The SSM agent does not run as a separate container sidecar, it runs as an additional process inside the application container.
- Best practice, we suggest to set the initProcessEnabled parameter to `true` in task definition to avoid SSM agent child processes becoming orphaned.


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
| [aws_efs_file_system.efs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/efs_file_system) | resource |
| [aws_efs_mount_target.efs-mt](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/efs_mount_target) | resource |
| [aws_security_group.efs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_security_group_rule.all_egress](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group_rule) | resource |
| [aws_availability_zones.available](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/availability_zones) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_efs_subnet_ids"></a> [efs\_subnet\_ids](#input\_efs\_subnet\_ids) | Provide list private subnets to use in this VPC. Example 10.0.10.0/24,10.0.11.0/24 | `list(string)` | n/a | yes |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_project"></a> [project](#input\_project) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | VPC Id to to launch the ALB | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_efs_security_group_id"></a> [efs\_security\_group\_id](#output\_efs\_security\_group\_id) | Security group outputs |
<!-- END_TF_DOCS -->