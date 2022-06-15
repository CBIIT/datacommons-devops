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
| [aws_lb.alb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb) | resource |
| [aws_lb_listener.listener_https](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener) | resource |
| [aws_lb_listener.redirect_https](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener) | resource |
| [aws_acm_certificate.cert](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/acm_certificate) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_acm_certificate_issued_type"></a> [acm\_certificate\_issued\_type](#input\_acm\_certificate\_issued\_type) | specify the issue type of the acm certificate, allowed values are AMAZON\_ISSUED & IMPORTED | `string` | `"AMAZON_ISSUED"` | no |
| <a name="input_alb_log_bucket_name"></a> [alb\_log\_bucket\_name](#input\_alb\_log\_bucket\_name) | s3 | `string` | n/a | yes |
| <a name="input_alb_name"></a> [alb\_name](#input\_alb\_name) | Name for the ALB | `string` | `"alb"` | no |
| <a name="input_alb_security_group_ids"></a> [alb\_security\_group\_ids](#input\_alb\_security\_group\_ids) | list of alb security groups | `list(string)` | n/a | yes |
| <a name="input_alb_subnet_ids"></a> [alb\_subnet\_ids](#input\_alb\_subnet\_ids) | list of subnets to use for the alb | `list(string)` | n/a | yes |
| <a name="input_certificate_domain_name"></a> [certificate\_domain\_name](#input\_certificate\_domain\_name) | domain name for the ssl cert | `string` | n/a | yes |
| <a name="input_default_message"></a> [default\_message](#input\_default\_message) | default message response from alb when resource is not available | `string` | `"The requested resource is not found"` | no |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_internal_alb"></a> [internal\_alb](#input\_internal\_alb) | is this alb internal? | `bool` | `false` | no |
| <a name="input_lb_type"></a> [lb\_type](#input\_lb\_type) | Type of loadbalancer | `string` | `"application"` | no |
| <a name="input_region"></a> [region](#input\_region) | aws region to deploy | `string` | `"us-east-1"` | no |
| <a name="input_ssl_policy"></a> [ssl\_policy](#input\_ssl\_policy) | specify ssl policy to use | `string` | `"ELBSecurityPolicy-2016-08"` | no |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | VPC Id to to launch the ALB | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_alb_dns_name"></a> [alb\_dns\_name](#output\_alb\_dns\_name) | ALB dns name |
| <a name="output_alb_https_listener_arn"></a> [alb\_https\_listener\_arn](#output\_alb\_https\_listener\_arn) | https listener arn |
| <a name="output_alb_zone_id"></a> [alb\_zone\_id](#output\_alb\_zone\_id) | https listener arn |
<!-- END_TF_DOCS -->