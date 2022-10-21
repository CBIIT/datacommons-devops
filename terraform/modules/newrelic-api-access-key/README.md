<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_newrelic"></a> [newrelic](#provider\_newrelic) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [newrelic_api_access_key.this](https://registry.terraform.io/providers/hashicorp/newrelic/latest/docs/resources/api_access_key) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app"></a> [app](#input\_app) | The name of the application (i.e. 'mtp') | `string` | n/a | yes |
| <a name="input_level"></a> [level](#input\_level) | The account level - either 'nonprod' or 'prod' are accepted | `string` | n/a | yes |
| <a name="input_new_relic_account_id"></a> [new\_relic\_account\_id](#input\_new\_relic\_account\_id) | The Leidos New Relic account id. If omitted, will default to account\_id specified in the provider | `number` | n/a | yes |
| <a name="input_new_relic_ingest_type"></a> [new\_relic\_ingest\_type](#input\_new\_relic\_ingest\_type) | Valid options are BROWSER or LICENSE | `string` | `"LICENSE"` | no |
| <a name="input_new_relic_key_type"></a> [new\_relic\_key\_type](#input\_new\_relic\_key\_type) | The type of API Key to create. Can be INGEST or USER | `string` | `"INGEST"` | no |
| <a name="input_program"></a> [program](#input\_program) | The name of the program (i.e. 'ccdi') | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_api_key"></a> [api\_key](#output\_api\_key) | n/a |
<!-- END_TF_DOCS -->