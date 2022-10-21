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
| [newrelic_cloud_aws_link_account.this](https://registry.terraform.io/providers/hashicorp/newrelic/latest/docs/resources/cloud_aws_link_account) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_id"></a> [account\_id](#input\_account\_id) | The AWS Account ID that the IAM role was provisioned to | `string` | n/a | yes |
| <a name="input_app"></a> [app](#input\_app) | The name of the application (i.e. 'mtp') | `string` | n/a | yes |
| <a name="input_iam_prefix"></a> [iam\_prefix](#input\_iam\_prefix) | The prefix used for all IAM resources created in Cloud One | `string` | `"power-user"` | no |
| <a name="input_level"></a> [level](#input\_level) | The account level - either 'nonprod' or 'prod' are accepted | `string` | n/a | yes |
| <a name="input_new_relic_account_id"></a> [new\_relic\_account\_id](#input\_new\_relic\_account\_id) | The Leidos New Relic account id. If omitted, will default to account\_id specified in the provider | `number` | n/a | yes |
| <a name="input_new_relic_metric_collection_mode"></a> [new\_relic\_metric\_collection\_mode](#input\_new\_relic\_metric\_collection\_mode) | How New Relic receives metrics from source - either PUSH or PULL | `string` | `"PUSH"` | no |
| <a name="input_program"></a> [program](#input\_program) | The name of the program (i.e. 'ccdi') | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_external_id"></a> [external\_id](#output\_external\_id) | n/a |
<!-- END_TF_DOCS -->