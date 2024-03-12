# Amazon OpenSearch Implementation Guide: 

# Basic Usage

<pre><code>module "opensearch" {
  source = "../.."

  attach_permissions_boundary = true
  cluster_tshirt_size         = "md"
  engine_version              = "OpenSearch_2.11"
  resource_prefix             = "program-tier-app"
  s3_snapshot_bucket_arn      = "arn:aws:s3:::basic-example-snapshot-bucket"
  subnet_ids                  = ["subnet-01234567891011121", "subnet-abcdefghijklmnopq"]
  vpc_id                      = "vpc-01234567891011121"
}</code></pre>

# Terraform Documentation

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
| [aws_cloudwatch_log_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_resource_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_resource_policy) | resource |
| [aws_iam_policy.snapshot](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.snapshot](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.snapshot](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_opensearch_domain.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearch_domain) | resource |
| [aws_security_group.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_security_group_rule.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group_rule) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.access_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.logs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.snapshot](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_iam_policy_document.trust](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_access_policies"></a> [access\_policies](#input\_access\_policies) | Required if create\_access\_policies is false. Provide json output from IAM Policy Document | `string` | `null` | no |
| <a name="input_attach_permissions_boundary"></a> [attach\_permissions\_boundary](#input\_attach\_permissions\_boundary) | Whether to attach the permissions boundary to the OpenSearch Snapshot Role | `bool` | `false` | no |
| <a name="input_auto_software_update_enabled"></a> [auto\_software\_update\_enabled](#input\_auto\_software\_update\_enabled) | Whether automatic service software updates are enabled for the domain | `bool` | `false` | no |
| <a name="input_auto_tune_enabled"></a> [auto\_tune\_enabled](#input\_auto\_tune\_enabled) | Whether to enable the OpenSearch Auto-Tune feature | `bool` | `true` | no |
| <a name="input_automated_snapshot_start_hour"></a> [automated\_snapshot\_start\_hour](#input\_automated\_snapshot\_start\_hour) | hour when automated snapshot to be taken | `number` | `5` | no |
| <a name="input_cluster_tshirt_size"></a> [cluster\_tshirt\_size](#input\_cluster\_tshirt\_size) | Select a T-Shirt size for the cluster | `string` | `"xs"` | no |
| <a name="input_cold_storage_enabled"></a> [cold\_storage\_enabled](#input\_cold\_storage\_enabled) | Boolean to enable cold storage for an OpenSearch domain. Master and ultrawarm nodes must be enabled for cold storage. | `bool` | `false` | no |
| <a name="input_create_access_policies"></a> [create\_access\_policies](#input\_create\_access\_policies) | Whether to allow the module to create the access policies for the OpenSearch domain | `bool` | `true` | no |
| <a name="input_create_cloudwatch_log_policy"></a> [create\_cloudwatch\_log\_policy](#input\_create\_cloudwatch\_log\_policy) | Whether to allow the module to create the cloudwatch log policy for the OpenSearch domain | `bool` | `true` | no |
| <a name="input_create_security_group"></a> [create\_security\_group](#input\_create\_security\_group) | Whether to allow the module to create the security group for the OpenSearch domain | `bool` | `true` | no |
| <a name="input_create_snapshot_role"></a> [create\_snapshot\_role](#input\_create\_snapshot\_role) | Whether to allow the module to create the snapshot role for the OpenSearch domain | `bool` | `true` | no |
| <a name="input_dedicated_master_count"></a> [dedicated\_master\_count](#input\_dedicated\_master\_count) | The number of Dedicated Master nodes in the cluster | `number` | `null` | no |
| <a name="input_dedicated_master_enabled"></a> [dedicated\_master\_enabled](#input\_dedicated\_master\_enabled) | Whether to enable Dedicated Master nodes in the cluster | `bool` | `false` | no |
| <a name="input_dedicated_master_type"></a> [dedicated\_master\_type](#input\_dedicated\_master\_type) | The instance type of the Dedicated Master nodes in the cluster | `string` | `null` | no |
| <a name="input_encrypt_at_rest"></a> [encrypt\_at\_rest](#input\_encrypt\_at\_rest) | Whether to enable encryption at rest for the domain | `bool` | `true` | no |
| <a name="input_enforce_https"></a> [enforce\_https](#input\_enforce\_https) | Whether to require HTTPS for all traffic to the domain | `bool` | `true` | no |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | The engine version of the OpenSearch domain (i.e., OpenSearch\_2.11) | `string` | n/a | yes |
| <a name="input_iam_prefix"></a> [iam\_prefix](#input\_iam\_prefix) | Prefix for IAM resource names | `string` | `"power-user"` | no |
| <a name="input_instance_count"></a> [instance\_count](#input\_instance\_count) | The number of Data Nodes attached to the cluster in each availability zone | `number` | `null` | no |
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | The instance type of the Data Nodes in the cluster | `string` | `null` | no |
| <a name="input_log_retention_in_days"></a> [log\_retention\_in\_days](#input\_log\_retention\_in\_days) | The number of days to retain OpenSearch logs in CloudWatch Logs | `number` | `180` | no |
| <a name="input_log_types"></a> [log\_types](#input\_log\_types) | The type of OpenSearch logs that will be published to CloudWatch Logs | `set(string)` | <pre>[<br>  "INDEX_SLOW_LOGS",<br>  "SEARCH_SLOW_LOGS",<br>  "ES_APPLICATION_LOGS"<br>]</pre> | no |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | Prefix for resource names, advised to use the program-tier-app convention | `string` | n/a | yes |
| <a name="input_s3_snapshot_bucket_arn"></a> [s3\_snapshot\_bucket\_arn](#input\_s3\_snapshot\_bucket\_arn) | The ARN of the S3 bucket to store OpenSearch snapshots | `string` | `null` | no |
| <a name="input_security_group_ids"></a> [security\_group\_ids](#input\_security\_group\_ids) | A set of one or more Security Group IDs to associate with the cluster | `set(string)` | `[]` | no |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | A set of one or more Private Subnet IDs to associate with the cluster | `set(string)` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | `{}` | no |
| <a name="input_tls_security_policy"></a> [tls\_security\_policy](#input\_tls\_security\_policy) | The name of the TLS security policy to apply to the domain | `string` | `"Policy-Min-TLS-1-2-PFS-2023-10"` | no |
| <a name="input_volume_size"></a> [volume\_size](#input\_volume\_size) | The size of the EBS volumes attached to data nodes (in GB) - between 10 and 200 | `number` | `null` | no |
| <a name="input_volume_type"></a> [volume\_type](#input\_volume\_type) | The volume type to use for data and master nodes | `string` | `"gp3"` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | the ID of the VPC the OpenSearch cluster is being deployed into | `string` | n/a | yes |
| <a name="input_warm_count"></a> [warm\_count](#input\_warm\_count) | The total number of warm nodes attached to the cluster | `number` | `null` | no |
| <a name="input_warm_enabled"></a> [warm\_enabled](#input\_warm\_enabled) | Whether to enable warm nodes in the cluster | `bool` | `false` | no |
| <a name="input_warm_type"></a> [warm\_type](#input\_warm\_type) | The instance type of the warm nodes in the cluster | `string` | `null` | no |
| <a name="input_zone_awareness_enabled"></a> [zone\_awareness\_enabled](#input\_zone\_awareness\_enabled) | Whether to enable Multi-AZ cluster deployment | `bool` | `false` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_arn"></a> [arn](#output\_arn) | The ARN of the OpenSearch domain |
| <a name="output_dashboard_endpoint"></a> [dashboard\_endpoint](#output\_dashboard\_endpoint) | The endpoint of the OpenSearch domain dashboard |
| <a name="output_domain_id"></a> [domain\_id](#output\_domain\_id) | The unique identifier for the OpenSearch domain |
| <a name="output_domain_name"></a> [domain\_name](#output\_domain\_name) | The name of the OpenSearch domain |
| <a name="output_endpoint"></a> [endpoint](#output\_endpoint) | The domain-specific endpoint used to submit index, search, and data upload requests to an OpenSearch domain |
| <a name="output_id"></a> [id](#output\_id) | The unique identifier for the OpenSearch domain |
| <a name="output_role_arn"></a> [role\_arn](#output\_role\_arn) | The ARN of the IAM role used to take snapshots of the OpenSearch domain |
| <a name="output_role_id"></a> [role\_id](#output\_role\_id) | The ID of the IAM role used to take snapshots of the OpenSearch domain |
| <a name="output_role_name"></a> [role\_name](#output\_role\_name) | The name of the IAM role used to take snapshots of the OpenSearch domain |
| <a name="output_security_group_arn"></a> [security\_group\_arn](#output\_security\_group\_arn) | The ARN of the security group for the OpenSearch domain |
| <a name="output_security_group_id"></a> [security\_group\_id](#output\_security\_group\_id) | The ID of the security group for the OpenSearch domain |
<!-- END_TF_DOCS -->

# Implementation Guide
The following guide provides a reference for OpenSearch service implementations aligned with NCI, NIST, and CTOS standards. 

## Service-Linked Role 
The OpenSearch service requires a service-linked role to be created in order to manage the OpenSearch cluster. The service-linked role is not created by the module, and therefore Terraform will return an error on the first apply. Simply execute the Terraform Apply workflow again to resolve the issue. Upon the failure on the initial apply, the service-linked role will be created and the apply will succeed on the second attempt.

## OpenSearch Manual Snapshots
By default, this module creates the IAM resources required to perform OpenSearch manual snapshot operations. Creation of the IAM resources can be disabled by setting the variable named `create_snapshot_role` to `false`. Please note that the module does not create an S3 bucket to store the snapshots, but provides the variable named `s3_snapshot_bucket_arn`. The project must create the S3 bucket and pass the ARN to the module.

## Security Group
By default, this module creates a security group for the OpenSearch cluster which can be disabled by setting the variable named `create_security_group` to `false` and providing one or more security group identifiers for the variable named `security_group_ids`. The security group is created with no ingress rules attached, but does create an egress rule allowing all outbound traffic. The project must attach the ingress rules to the security group by referencing the `security_group_id` output. 

## Standard Cluster Sizing Configurations
The CTOS program establishes pre-determined cluster sizing configurations for OpenSearch to simplify implementation and achieve cross-program standardization. T-Shirt sizes influence the instance type and EBS storage volume sizes. Please note: the storage sizes are per node, and the default node count is 1 data node.

| Size  | vCPU  | Memory  | Storage |
| :---: | :---: |  :---:  |  :---:  |
| `xs`  | 2     | 2 GB    | 10 GB   |
| `sm`  | 2     | 4 GB    | 20 GB   |
| `md`  | 2     | 8 GB    | 40 GB   |
| `lg`  | 4     | 16 GB   | 80 GB   |
| `xl`  | 8     | 32 GB   | 160 GB  |

If you select a T-Shirt size for the variable named `cluster_tshirt_size`, then you do not have to specify the `volume_size` or `instance_type` variables. The module will automatically select the appropriate instance type and storage volume size based on the T-Shirt size selected. Providing a value for the `volume_size` or `instance_type` variables will override the T-Shirt size selection. You can also specify `instance_count` to increase the number of data nodes in the cluster.

## Choosing a Cluster T-Shirt Size
Consider the following factors when choosing a cluster T-Shirt size:
1. The target storage utilization should be no more than 70% of the total storage capacity.
2. The estimated size of any index should not be larger than 50% of a single node's storage capacity.

### Example Scenario 1:
A project anticipates `5` indexes that will be stored in OpenSearch. Each of the five indexes are anticipated to be 1 GB in size. 
- Total Storage Required: `5 GB`
- Largest Index Size: `1 GB`
- T-Shirt Size Recommendation: `xs`

### Example Scenario 2:
A project anticipates 2 indexes that will be stored in OpenSearch. One index is anticipated to be 6 GB in size. The other index is anticipated to be 0.5 GB in size.
- Total Storage Required: `6.5 GB`
- Largest Index Size: `6 GB`
- T-Shirt Size Recommendation: `sm`


## Multi-AZ Deployments
By default, this module creates a single data node in a Single AWS Availability Zone (AZ). To configure the cluster for a Multi-AZ deployment, set the variable named `zone_awareness_enabled` to `true`. Be aware that Multi-AZ deployments will double the number of Data Nodes in the cluster. 

## Domain Access Policies
By default, this module creates and attaches an OpenSearch Domain Access Policy that allows HTTPS-based actions to be performed by any AWS principal. The policy can be disabled by setting the variable named `create_access_policies` to `false`. If you disable the access policy, you must provide your own access policy for the variable named `access_policies`. The value of the `access_policies` variable must be a valid JSON string, which can be produced from using a `data.iam_policy_document.{name}.json` data source reference.

## Cluster Log Monitoring
By default, the cluster has logging configured, and all types of logs generated by the cluster are forwarded to a CloudWatch Log Group created by the module. The logs that are generated are described below.
- Index Slow Logs: Logs that are generated when indexing operations take longer than the index.indexing\_slowlog.threshold.index.warn value.
- Search Slow Logs: Logs that are generated when search operations take longer than the index.search\_slowlog.threshold.query.warn value.
- Application Logs: Error logs that are generated by the OpenSearch cluster.