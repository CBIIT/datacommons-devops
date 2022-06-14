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
| <a name="input_microservices"></a> [microservices](#input\_microservices) | n/a | <pre>map(object({<br>    name = string<br>    port = number<br>    health_check_path = string<br>    priority_rule_number = number<br>    image_url = string<br>    cpu = number<br>    memory = number<br>    path = string<br>    number_container_replicas = number<br>  }))</pre> | n/a | yes |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | VPC Id to to launch the ALB | `string` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->