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
| [aws_route53_record.dns_record](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route53_record) | resource |
| [aws_route53_zone.zone](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/route53_zone) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_alb_dns_name"></a> [alb\_dns\_name](#input\_alb\_dns\_name) | alb dns name | `string` | n/a | yes |
| <a name="input_alb_zone_id"></a> [alb\_zone\_id](#input\_alb\_zone\_id) | alb dns name | `string` | n/a | yes |
| <a name="input_application_subdomain"></a> [application\_subdomain](#input\_application\_subdomain) | subdomain of the app | `string` | n/a | yes |
| <a name="input_domain_name"></a> [domain\_name](#input\_domain\_name) | domain name for the application | `string` | n/a | yes |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_application_dns_name"></a> [application\_dns\_name](#output\_application\_dns\_name) | n/a |
| <a name="output_application_fqdn"></a> [application\_fqdn](#output\_application\_fqdn) | n/a |
<!-- END_TF_DOCS -->