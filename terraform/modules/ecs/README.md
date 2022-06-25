# General Notes/Comments:
- I think we're creating target groups in the ALB and the ECS modules - should we pick one? ECS makes most sense.

# Setting up ECS Exec
- It’s important to notice that the container image requires `script` (part of util-linux) and `cat` (part of coreutils) to be installed in order to have command logs uploaded correctly to S3 and/or CloudWatch. The nginx container images have this support already installed. 
- The SSM agent does not run as a separate container sidecar, it runs as an additional process inside the application container.
- ECS Task role needs to allow communications with SSM and CloudWatch
- Need to create a SG rule that allows ingress with tcp over port 80 with cidr 0.0.0.0/0




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
| [aws_appautoscaling_policy.microservice_autoscaling_cpu](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appautoscaling_policy) | resource |
| [aws_appautoscaling_target.microservice_autoscaling_target](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appautoscaling_target) | resource |
| [aws_ecs_cluster.ecs_cluster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_cluster) | resource |
| [aws_ecs_service.service](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_service) | resource |
| [aws_ecs_task_definition.task](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_task_definition) | resource |
| [aws_lb_listener_rule.alb_listener](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener_rule) | resource |
| [aws_lb_target_group.target_group](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_target_group) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.ecs_exec_cloudwatch](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_exec_command](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_exec_kms](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_exec_s3](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_exec_ssm](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.ecs_trust_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_alb_https_listener_arn"></a> [alb\_https\_listener\_arn](#input\_alb\_https\_listener\_arn) | alb https listener arn | `string` | n/a | yes |
| <a name="input_alb_target_type"></a> [alb\_target\_type](#input\_alb\_target\_type) | type of alb target - ip , instance, lambda | `string` | `"ip"` | no |
| <a name="input_application_url"></a> [application\_url](#input\_application\_url) | url of the application | `string` | n/a | yes |
| <a name="input_ecs_execution_role_arn"></a> [ecs\_execution\_role\_arn](#input\_ecs\_execution\_role\_arn) | ecs execution iam role arn | `string` | n/a | yes |
| <a name="input_ecs_launch_type"></a> [ecs\_launch\_type](#input\_ecs\_launch\_type) | ecs launch type - FARGATE or EC2 | `string` | `"FARGATE"` | no |
| <a name="input_ecs_network_mode"></a> [ecs\_network\_mode](#input\_ecs\_network\_mode) | ecs network mode - bridge,host,awsvpc | `string` | `"awsvpc"` | no |
| <a name="input_ecs_scheduling_strategy"></a> [ecs\_scheduling\_strategy](#input\_ecs\_scheduling\_strategy) | ecs scheduling strategy | `string` | `"REPLICA"` | no |
| <a name="input_ecs_security_group_ids"></a> [ecs\_security\_group\_ids](#input\_ecs\_security\_group\_ids) | list of security groups to apply to this ecs | `list(string)` | n/a | yes |
| <a name="input_ecs_subnet_ids"></a> [ecs\_subnet\_ids](#input\_ecs\_subnet\_ids) | Provide list private subnets to use in this VPC. Example 10.0.10.0/24,10.0.11.0/24 | `list(string)` | n/a | yes |
| <a name="input_ecs_task_role_arn"></a> [ecs\_task\_role\_arn](#input\_ecs\_task\_role\_arn) | ecs task iam role arn | `string` | n/a | yes |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_microservices"></a> [microservices](#input\_microservices) | n/a | <pre>map(object({<br>    name                      = string<br>    port                      = number<br>    health_check_path         = string<br>    priority_rule_number      = number<br>    image_url                 = string<br>    cpu                       = number<br>    memory                    = number<br>    path                      = string<br>    number_container_replicas = number<br>  }))</pre> | n/a | yes |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | VPC Id to to launch the ALB | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->