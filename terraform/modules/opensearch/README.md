# Amazon OpenSearch Implementation Guide: 

# Basic Usage

<pre><code>module "opensearch" {
  source = "../.."

  domain_name                 = "program-tier-app-opensearch"
  attach_permissions_boundary = true
  cluster_tshirt_size         = "md"
  engine_version              = "OpenSearch_2.11"
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
| [aws_cloudwatch_log_group.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_cloudwatch_log_resource_policy.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_resource_policy) | resource |
| [aws_iam_service_linked_role.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_service_linked_role) | resource |
| [aws_opensearch_domain.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearch_domain) | resource |
| [aws_security_group.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_caller_identity.caller](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_iam_policy_document.os](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |
| [aws_region.region](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_automated_snapshot_start_hour"></a> [automated\_snapshot\_start\_hour](#input\_automated\_snapshot\_start\_hour) | hour when automated snapshot to be taken | `number` | `23` | no |
| <a name="input_create_cloudwatch_log_policy"></a> [create\_cloudwatch\_log\_policy](#input\_create\_cloudwatch\_log\_policy) | Due cloudwatch log policy limits, this should be option, we can use an existing policy | `bool` | `false` | no |
| <a name="input_create_os_service_role"></a> [create\_os\_service\_role](#input\_create\_os\_service\_role) | change this value to true if running this script for the first time | `bool` | `false` | no |
| <a name="input_env"></a> [env](#input\_env) | name of the environment to provision | `string` | n/a | yes |
| <a name="input_multi_az_enabled"></a> [multi\_az\_enabled](#input\_multi\_az\_enabled) | set to true to enable multi-az deployment | `bool` | `false` | no |
| <a name="input_opensearch_autotune_rollback_type"></a> [opensearch\_autotune\_rollback\_type](#input\_opensearch\_autotune\_rollback\_type) | Tell OpenSearch how to respond to disabling AutoTune. Options include NO\_ROLLBACK and DEFAULT\_ROLLBACK | `string` | `"DEFAULT_ROLLBACK"` | no |
| <a name="input_opensearch_autotune_state"></a> [opensearch\_autotune\_state](#input\_opensearch\_autotune\_state) | Tell OpenSearch to enable or disable autotuning. Options include ENABLED and DISABLED | `string` | `"ENABLED"` | no |
| <a name="input_opensearch_ebs_volume_size"></a> [opensearch\_ebs\_volume\_size](#input\_opensearch\_ebs\_volume\_size) | size of the ebs volume attached to the opensearch instance | `number` | `30` | no |
| <a name="input_opensearch_instance_count"></a> [opensearch\_instance\_count](#input\_opensearch\_instance\_count) | the number of data nodes to provision for each instance in the cluster | `number` | `1` | no |
| <a name="input_opensearch_instance_type"></a> [opensearch\_instance\_type](#input\_opensearch\_instance\_type) | type of instance to be used to create the OpenSearch cluster | `string` | `"t3.medium.search"` | no |
| <a name="input_opensearch_log_types"></a> [opensearch\_log\_types](#input\_opensearch\_log\_types) | List of log types that OpenSearch forwards to CloudWatch. Options include INDEX\_SLOW\_LOGS, SEARCH\_SLOW\_LOGS, ES\_APPLICATION\_LOGS, AUDIT\_LOGS | `list(string)` | <pre>[<br>  "AUDIT_LOGS"<br>]</pre> | no |
| <a name="input_opensearch_subnet_ids"></a> [opensearch\_subnet\_ids](#input\_opensearch\_subnet\_ids) | list of subnet ids to use | `list(string)` | n/a | yes |
| <a name="input_opensearch_tls_policy"></a> [opensearch\_tls\_policy](#input\_opensearch\_tls\_policy) | Provide the TLS policy to associate with the OpenSearch domain to enforce HTTPS communications | `string` | `"Policy-Min-TLS-1-2-2019-07"` | no |
| <a name="input_opensearch_version"></a> [opensearch\_version](#input\_opensearch\_version) | specify es version | `string` | `"OpenSearch_1.2"` | no |
| <a name="input_resource_prefix"></a> [resource\_prefix](#input\_resource\_prefix) | the prefix to add when creating resources | `string` | n/a | yes |
| <a name="input_stack_name"></a> [stack\_name](#input\_stack\_name) | name of the project | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to associate with this instance | `map(string)` | n/a | yes |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | the ID of the VPC the OpenSearch cluster is being deployed into | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_opensearch_arn"></a> [opensearch\_arn](#output\_opensearch\_arn) | the OpenSearch domain arn |
| <a name="output_opensearch_cloudwatch_log_group_arn"></a> [opensearch\_cloudwatch\_log\_group\_arn](#output\_opensearch\_cloudwatch\_log\_group\_arn) | the log group arn that collects OpenSearch logs |
| <a name="output_opensearch_endpoint"></a> [opensearch\_endpoint](#output\_opensearch\_endpoint) | the opensearch domain endpoint url |
| <a name="output_opensearch_security_group_arn"></a> [opensearch\_security\_group\_arn](#output\_opensearch\_security\_group\_arn) | the arn of the security group associated with the OpenSearch cluster |
| <a name="output_opensearch_security_group_id"></a> [opensearch\_security\_group\_id](#output\_opensearch\_security\_group\_id) | the id of the security group associated with the OpenSearch cluster |
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