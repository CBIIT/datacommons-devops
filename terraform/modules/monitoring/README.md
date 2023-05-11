<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_sumologic"></a> [sumologic](#provider\_sumologic) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [sumologic_collector.collector](https://registry.terraform.io/providers/sumologic/sumologic/latest/docs/resources/collector) | resource |
| [sumologic_http_source.sumo_source](https://registry.terraform.io/providers/sumologic/sumologic/latest/docs/resources/http_source) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app"></a> [app](#input\_app) | name of the app | `string` | n/a | yes |
| <a name="input_microservices"></a> [microservices](#input\_microservices) | n/a | <pre>map(object({<br>    name                      = string<br>    port                      = number<br>    health_check_path         = string<br>    priority_rule_number      = number<br>    image_url                 = string<br>    cpu                       = number<br>    memory                    = number<br>    path                      = list(string)<br>    number_container_replicas = number<br>  }))</pre> | n/a | yes |
| <a name="input_newrelic_account_id"></a> [newrelic\_account\_id](#input\_newrelic\_account\_id) | New Relic Account ID | `string` | n/a | yes |
| <a name="input_newrelic_api_key"></a> [newrelic\_api\_key](#input\_newrelic\_api\_key) | New Relic API Key | `string` | n/a | yes |
| <a name="input_program"></a> [program](#input\_program) | Name of the program where the application is running. example ccdi or crdc etc | `string` | n/a | yes |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | the prefix to add when creating resources | `string` | n/a | yes |
| <a name="input_service"></a> [service](#input\_service) | Name of the service where the monitoring is configured. example ecs, database etc | `string` | n/a | yes |
| <a name="input_sumologic_access_id"></a> [sumologic\_access\_id](#input\_sumologic\_access\_id) | Sumo Logic Access ID | `string` | n/a | yes |
| <a name="input_sumologic_access_key"></a> [sumologic\_access\_key](#input\_sumologic\_access\_key) | Sumo Logic Access Key | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_sumo_source_urls"></a> [sumo\_source\_urls](#output\_sumo\_source\_urls) | map of name, source url for sumo collectors |
<!-- END_TF_DOCS -->