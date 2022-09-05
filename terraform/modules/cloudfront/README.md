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
| [aws_cloudfront_distribution.distribution](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_distribution) | resource |
| [aws_cloudfront_origin_access_identity.origin_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_origin_access_identity) | resource |
| [aws_s3_bucket_cors_configuration.cors](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_cors_configuration) | resource |
| [aws_s3_bucket_policy.bucket_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_policy) | resource |
| [aws_cloudfront_cache_policy.managed_cache](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/cloudfront_cache_policy) | data source |
| [aws_cloudfront_origin_request_policy.s3_cors](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/cloudfront_origin_request_policy) | data source |
| [aws_iam_policy_document.s3_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_s3_bucket.cloudfront_log_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/s3_bucket) | data source |
| [aws_s3_bucket.cloudfront_s3_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/s3_bucket) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cloudfront_distribution_bucket_name"></a> [cloudfront\_distribution\_bucket\_name](#input\_cloudfront\_distribution\_bucket\_name) | specify the name of s3 bucket for cloudfront | `string` | n/a | yes |
| <a name="input_cloudfront_distribution_log_bucket_name"></a> [cloudfront\_distribution\_log\_bucket\_name](#input\_cloudfront\_distribution\_log\_bucket\_name) | specify the name of s3 bucket for the cloudfront logs | `string` | n/a | yes |
| <a name="input_cloudfront_log_path_prefix_key"></a> [cloudfront\_log\_path\_prefix\_key](#input\_cloudfront\_log\_path\_prefix\_key) | path prefix to where cloudfront send logs to s3 bucket | `string` | `"cloudfront/logs"` | no |
| <a name="input_cloudfront_origin_access_identity_description"></a> [cloudfront\_origin\_access\_identity\_description](#input\_cloudfront\_origin\_access\_identity\_description) | description for OAI | `string` | `"cloudfront origin access identify for s3"` | no |
| <a name="input_env"></a> [env](#input\_env) | environment | `string` | n/a | yes |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_cloudfront_distribution_endpoint"></a> [cloudfront\_distribution\_endpoint](#output\_cloudfront\_distribution\_endpoint) | n/a |
<!-- END_TF_DOCS -->