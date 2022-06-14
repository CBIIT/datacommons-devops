<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_s3"></a> [s3](#module\_s3) | terraform-aws-modules/s3-bucket/aws | 3.2.3 |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_attach_bucket_policy"></a> [attach\_bucket\_policy](#input\_attach\_bucket\_policy) | set to true if you want bucket policy and provide value for policy variable | `bool` | `false` | no |
| <a name="input_bucket_acl"></a> [bucket\_acl](#input\_bucket\_acl) | type of bucket acl to apply | `string` | `"private"` | no |
| <a name="input_bucket_name"></a> [bucket\_name](#input\_bucket\_name) | name of the s3 bucket | `string` | n/a | yes |
| <a name="input_bucket_policy"></a> [bucket\_policy](#input\_bucket\_policy) | s3 bucket policy | `any` | `[]` | no |
| <a name="input_enable_version"></a> [enable\_version](#input\_enable\_version) | enable bucket versioning | `bool` | `false` | no |
| <a name="input_force_destroy_bucket"></a> [force\_destroy\_bucket](#input\_force\_destroy\_bucket) | force destroy s3 bucket. | `bool` | `false` | no |
| <a name="input_lifecycle_rule"></a> [lifecycle\_rule](#input\_lifecycle\_rule) | object lifecycle rule | `any` | `[]` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this resource | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_bucket_name"></a> [bucket\_name](#output\_bucket\_name) | name of the bucket |
<!-- END_TF_DOCS -->