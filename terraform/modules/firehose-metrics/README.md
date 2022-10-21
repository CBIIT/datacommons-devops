# AWS-Managed Services Metric Collection

This module's purpose is to streamline the implementation of a metric delivery pipeline to support observability of AWS Managed Services that publish metric data to Amazon CloudWatch. The destination of the metric data collected is New Relic, FNL/CTOS' preferred metric observability platform. 

## Resources Provided by the Module

  - Amazon CloudWatch Metric Stream
  - AWS Kinesis Data Firehose Delivery Stream
  - Amazon Identity and Access Management Roles

## Resources Not Provided by the Module

  - Amazon Simple Storage Solution (S3 Bucket)
  - Metric Data Producers

## Requirements Prior to Implementation
  - Access to the CTOS New Relic Instance
  - New Relic permissions to register a new AWS account

## Solution Overview
![newrelic metric delivery pipeline diagram](./assets/diagram.png)

## Usage Examples

Please note that the following are just examples. The example values provided for the access keys, external IDs, etc. are fictitious. 

### Minimum Configuration 
<pre><code>module "new_relic_metric_pipeline" {
  source = "github.com/CBIIT/datacommons-devops/terraform/modules/firehose-metrics/"

  account_id                = data.aws_caller_identity.current.account_id
  app                       = "icdc"
  http_endpoint_access_key  = "KL3SDFJ6VX53QOROERTIBMCLPI2R39_" 
  level                     = "non-prod"
  new_relic_account_id      = 123456789101
  new_relic_external_id     = 987654
  permission_boundary_arn   = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
  program                   = "crdc"
  s3_bucket_arn             = "arn:aws:s3:::example-icdc-destination-bucket"
}</code></pre>

### Maximum Configuration
<pre><code>module "new_relic_metric_pipeline" {
  source = "github.com/CBIIT/datacommons-devops/terraform/modules/firehose-metrics/"

  account_id                = data.aws_caller_identity.current.account_id
  app                       = "icdc"
  buffer_interval           = 60
  buffer_size               = 1
  content_encoding          = "GZIP"
  destination               = "http_endpoint"
  force_detach_policies     = false
  http_endpoint_access_key  = "KL3SDFJ6VX53QOROERTIBMCLPI2R39_" 
  iam_prefix                = "power-user"
  include_filter            = [ "AWS/ES", "AWS/ApplicationELB" ]
  level                     = "non-prod"
  output_format             = "opentelemetry0.7
  new_relic_account_id      = 123456789101
  new_relic_external_id     = 987654
  permission_boundary_arn   = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
  program                   = "crdc"
  s3_backup_mode            = "FailedDataOnly"
  s3_bucket_arn             = "arn:aws:s3:::example-icdc-destination-bucket"
  s3_compression_format     = "UNCOMPRESSED"
  s3_error_output_prefix    = null 
  s3_object_prefix          = null
}</code></pre>


<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.3 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 4.0.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_cloudwatch_metric_stream"></a> [cloudwatch\_metric\_stream](#module\_cloudwatch\_metric\_stream) | ./modules/cloudwatch-metric-stream | n/a |
| <a name="module_iam_cloudwatch_metric_stream"></a> [iam\_cloudwatch\_metric\_stream](#module\_iam\_cloudwatch\_metric\_stream) | ./modules/iam-cloudwatch-metric-stream | n/a |
| <a name="module_iam_kinesis_firehose_datastream"></a> [iam\_kinesis\_firehose\_datastream](#module\_iam\_kinesis\_firehose\_datastream) | ./modules/iam-kinesis-firehose-datastream | n/a |
| <a name="module_iam_read_only"></a> [iam\_read\_only](#module\_iam\_read\_only) | ./modules/iam-read-only | n/a |
| <a name="module_kinesis_firehose_datastream"></a> [kinesis\_firehose\_datastream](#module\_kinesis\_firehose\_datastream) | ./modules/kinesis-firehose-datastream | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_id"></a> [account\_id](#input\_account\_id) | The ID of the target account (use data.aws\_caller\_identity.current.account\_id) | `string` | n/a | yes |
| <a name="input_app"></a> [app](#input\_app) | The name of the application (i.e. 'mtp') | `string` | n/a | yes |
| <a name="input_buffer_interval"></a> [buffer\_interval](#input\_buffer\_interval) | Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination | `number` | `60` | no |
| <a name="input_buffer_size"></a> [buffer\_size](#input\_buffer\_size) | Buffer incoming data to the specified size, in MBs, before delivering it to the destination | `number` | `1` | no |
| <a name="input_content_encoding"></a> [content\_encoding](#input\_content\_encoding) | Kinesis Data Firehose uses the content encoding to compress the body of a request before sending the request to the destination - valid values are NONE and GZIP | `string` | `"GZIP"` | no |
| <a name="input_destination"></a> [destination](#input\_destination) | the destination to where the data is delivered. The only options are 'extended\_s3', 'redshift', 'elasticsearch', and 'http\_endpoint' | `string` | `"http_endpoint"` | no |
| <a name="input_force_detach_policies"></a> [force\_detach\_policies](#input\_force\_detach\_policies) | Set to true to automatically detach policies when deleting a role | `bool` | `false` | no |
| <a name="input_http_endpoint_access_key"></a> [http\_endpoint\_access\_key](#input\_http\_endpoint\_access\_key) | The New Relic api key (of type User) | `string` | n/a | yes |
| <a name="input_http_endpoint_name"></a> [http\_endpoint\_name](#input\_http\_endpoint\_name) | The HTTP endpoint name | `string` | `"New Relic"` | no |
| <a name="input_http_endpoint_url"></a> [http\_endpoint\_url](#input\_http\_endpoint\_url) | The HTTP endpoint URL to which Kinesis Firehose sends your data | `string` | `"https://gov-metric-api.newrelic.com/metric/v1"` | no |
| <a name="input_iam_prefix"></a> [iam\_prefix](#input\_iam\_prefix) | The string prefix for IAM resource name attributes | `string` | `"power-user"` | no |
| <a name="input_include_filter"></a> [include\_filter](#input\_include\_filter) | Specify the service namespaces to include in metric stream in a list | `set(string)` | <pre>[<br>  "AWS/ES",<br>  "AWS/ApplicationELB"<br>]</pre> | no |
| <a name="input_level"></a> [level](#input\_level) | The account level - either 'nonprod' or 'prod' are accepted | `string` | n/a | yes |
| <a name="input_new_relic_account_id"></a> [new\_relic\_account\_id](#input\_new\_relic\_account\_id) | The New Relic account ID | `number` | n/a | yes |
| <a name="input_new_relic_aws_account_id"></a> [new\_relic\_aws\_account\_id](#input\_new\_relic\_aws\_account\_id) | The standard New Relic AWS account identifier - nonsensitive | `string` | `"754728514883"` | no |
| <a name="input_new_relic_ingest_type"></a> [new\_relic\_ingest\_type](#input\_new\_relic\_ingest\_type) | Valid options are BROWSER or LICENSE | `string` | `"LICENSE"` | no |
| <a name="input_new_relic_key_type"></a> [new\_relic\_key\_type](#input\_new\_relic\_key\_type) | The type of API Key to create. Can be INGEST or USER | `string` | `"INGEST"` | no |
| <a name="input_new_relic_metric_collection_mode"></a> [new\_relic\_metric\_collection\_mode](#input\_new\_relic\_metric\_collection\_mode) | How New Relic receives metrics from source - either PUSH or PULL | `string` | `"PUSH"` | no |
| <a name="input_output_format"></a> [output\_format](#input\_output\_format) | Output format of the CloudWatch Metric Stream - can be json or opentelemetry0.7 | `string` | `"opentelemetry0.7"` | no |
| <a name="input_permission_boundary_arn"></a> [permission\_boundary\_arn](#input\_permission\_boundary\_arn) | The arn of the permission boundaries for roles. Set to null for prod account levels | `string` | n/a | yes |
| <a name="input_program"></a> [program](#input\_program) | The name of the program (i.e. 'ccdi') | `string` | n/a | yes |
| <a name="input_s3_backup_mode"></a> [s3\_backup\_mode](#input\_s3\_backup\_mode) | Defines how documents should be delivered to Amazon S3. Valid values are 'FailedDataOnly' and 'AllData' | `string` | `"FailedDataOnly"` | no |
| <a name="input_s3_bucket_arn"></a> [s3\_bucket\_arn](#input\_s3\_bucket\_arn) | The arn of the S3 bucket where failed message deliveries to New Relic are delivered | `string` | n/a | yes |
| <a name="input_s3_compression_format"></a> [s3\_compression\_format](#input\_s3\_compression\_format) | File compression format - values are 'GZIP', 'ZIP', 'Snappy', & 'HADOOP\_SNAPPY' | `string` | `"UNCOMPRESSED"` | no |
| <a name="input_s3_error_output_prefix"></a> [s3\_error\_output\_prefix](#input\_s3\_error\_output\_prefix) | Prefix added to failed records before writing them to S3 - immediately follows bucket name | `string` | `null` | no |
| <a name="input_s3_object_prefix"></a> [s3\_object\_prefix](#input\_s3\_object\_prefix) | The 'YYYY/MM/DD/HH' time format prefix is automatically used for delivered S3 files. You can specify an extra prefix to be added in front of the time format prefix | `string` | `null` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
