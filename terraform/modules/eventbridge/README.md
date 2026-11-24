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
| [aws_cloudwatch_event_rule.module_event](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.ecs_target](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_event_target.lambda_target](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_cloudwatch_log_group.eventbridge_log_group](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_stream.eventbridge_log_stream](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_stream) | resource |
| [aws_iam_role.eventbridge_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy.eventbridge_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_assign_public_ip"></a> [assign\_public\_ip](#input\_assign\_public\_ip) | Whether to assign a public IP to the ECS task. Valid values: 'ENABLED', 'DISABLED' | `string` | `"DISABLED"` | no |
| <a name="input_ecs_cluster_arn"></a> [ecs\_cluster\_arn](#input\_ecs\_cluster\_arn) | ARN of the ECS cluster for ECS task type targets | `string` | `""` | no |
| <a name="input_ecs_security_groups"></a> [ecs\_security\_groups](#input\_ecs\_security\_groups) | List of security group IDs for ECS task type targets | `list(string)` | `[]` | no |
| <a name="input_eventbridge_name"></a> [eventbridge\_name](#input\_eventbridge\_name) | Name of the EventBridge rule | `string` | n/a | yes |
| <a name="input_iam_prefix"></a> [iam\_prefix](#input\_iam\_prefix) | The string prefix for IAM roles and policies to conform to NCI power-user compliance | `string` | `"power-user"` | no |
| <a name="input_private_subnet_ids"></a> [private\_subnet\_ids](#input\_private\_subnet\_ids) | List of private subnet IDs for ECS task type targets | `list(string)` | `[]` | no |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | The prefix to add when creating resources | `string` | n/a | yes |
| <a name="input_role_arn"></a> [role\_arn](#input\_role\_arn) | The ARN of the IAM role to use for EventBridge. | `string` | n/a | yes |
| <a name="input_schedule_expression"></a> [schedule\_expression](#input\_schedule\_expression) | Schedule expression for the EventBridge rule | `string` | n/a | yes |
| <a name="input_target_account_cloudone"></a> [target\_account\_cloudone](#input\_target\_account\_cloudone) | to add check conditions on whether the resources are brought up in cloudone or not | `bool` | `true` | no |
| <a name="input_target_arn"></a> [target\_arn](#input\_target\_arn) | ARN of the EventBridge target | `string` | n/a | yes |
| <a name="input_target_type"></a> [target\_type](#input\_target\_type) | Type of the EventBridge target (e.g., 'ecs-task', 'lambda', 'sns') | `string` | n/a | yes |
| <a name="input_task_definition_arn"></a> [task\_definition\_arn](#input\_task\_definition\_arn) | ARN of the ECS task definition for ECS task type targets | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_eventbridge_ecs_target_id"></a> [eventbridge\_ecs\_target\_id](#output\_eventbridge\_ecs\_target\_id) | The ID of the EventBridge target for the ECS task. |
| <a name="output_eventbridge_lambda_target_id"></a> [eventbridge\_lambda\_target\_id](#output\_eventbridge\_lambda\_target\_id) | The ID of the EventBridge target for the Lambda function. |
| <a name="output_eventbridge_rule_name"></a> [eventbridge\_rule\_name](#output\_eventbridge\_rule\_name) | The name of the EventBridge rule. |
<!-- END_TF_DOCS -->