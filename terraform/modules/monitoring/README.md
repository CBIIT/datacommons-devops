<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 0.13 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_newrelic"></a> [newrelic](#provider\_newrelic) | n/a |
| <a name="provider_sumologic"></a> [sumologic](#provider\_sumologic) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [newrelic_one_dashboard.alb_dashboard](https://registry.terraform.io/providers/newrelic/newrelic/latest/docs/resources/one_dashboard) | resource |
| [newrelic_one_dashboard.fargate_dashboard](https://registry.terraform.io/providers/newrelic/newrelic/latest/docs/resources/one_dashboard) | resource |
| [newrelic_one_dashboard.os_dashboard](https://registry.terraform.io/providers/newrelic/newrelic/latest/docs/resources/one_dashboard) | resource |
| [sumologic_collector.collector](https://registry.terraform.io/providers/sumologic/sumologic/latest/docs/resources/collector) | resource |
| [sumologic_http_source.backend_source](https://registry.terraform.io/providers/sumologic/sumologic/latest/docs/resources/http_source) | resource |
| [sumologic_http_source.files_source](https://registry.terraform.io/providers/sumologic/sumologic/latest/docs/resources/http_source) | resource |
| [sumologic_http_source.frontend_source](https://registry.terraform.io/providers/sumologic/sumologic/latest/docs/resources/http_source) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app"></a> [app](#input\_app) | name of the app | `string` | n/a | yes |
| <a name="input_newrelic_account_id"></a> [newrelic\_account\_id](#input\_newrelic\_account\_id) | Newrelic Account ID | `string` | n/a | yes |
| <a name="input_newrelic_api_key"></a> [newrelic\_api\_key](#input\_newrelic\_api\_key) | Newrelic API Key | `string` | n/a | yes |
| <a name="input_sumologic_access_id"></a> [sumologic\_access\_id](#input\_sumologic\_access\_id) | Sumo Logic Access ID | `string` | n/a | yes |
| <a name="input_sumologic_access_key"></a> [sumologic\_access\_key](#input\_sumologic\_access\_key) | Sumo Logic Access Key | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_backend_source_url"></a> [backend\_source\_url](#output\_backend\_source\_url) | backend source url |
| <a name="output_files_source_url"></a> [files\_source\_url](#output\_files\_source\_url) | files source url |
| <a name="output_frontend_source_url"></a> [frontend\_source\_url](#output\_frontend\_source\_url) | frontend source url |
<!-- END_TF_DOCS -->