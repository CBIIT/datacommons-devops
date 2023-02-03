# AWS-Managed Services Metric Collection

This module's purpose is to streamline the implementation of a metric delivery pipeline to support observability of AWS Managed Services that publish metric data to Amazon CloudWatch. The destination of the metric data collected is New Relic, FNL/CTOS' preferred metric observability platform. 

## Solution Overview
![newrelic metric delivery pipeline diagram](./assets/diagram.png)

## Implementation Steps

### 1. Create a New Relic API Key
Log into https://one.newrelic.com/ and navigate to the API Keys page within the Administration module. Create a new API Key that is a "Ingest - License" type. Name the key with the following naming convention: program - account level - app (ie. ccdi-nonprod-mtp). Provide notes when creating the key as you see fit. Copy the key value to your clipboard. Please note, it's recommended that we have no more than one key that is used per account. 

### 2. Retrieve the New Relic Account ID
While logged into New Relic and within the Administration module, select the "Access Management" page and navigate to the "Accounts" tab. Copy the account ID for the account with the name "Leidos Biomedical Research_2". This, along with the New Relic API key, are the only New Relic-specific arguments to pass to the metric pipeline module. 

### 3. Configure Terraform Configuration
In your project repository, create the metric pipeline configuration that leverages this shared module. See the Usage Examples below for more details. Please note that two arguments (new_relic_account_id and http_endpoint_access_key) are not provided in the examples. To prevent storing sensitive information in GitHub repositories, it's recommended that those values are passed in during Terraform workflow operations, but can be configured to exist in a secret. 

It is also recommended that the state for the metric pipeline is stored separate from the rest of the project's configuration. This is because we will deploy the metric pipeline stack once per account, rather than once per tier. You may opt to use conditionals and include the stack in the same state shared with the rest of the project's infrastructure. 

### 4. Deploy the Stack
After configuring your project for the metric pipeline implementation, run through the standard Terraform workflow and provide the http_endpoint_access_key and new_relic_account_id variable values. 

### 5. Collect the Read-Only Role ARN
After deploying the stack, you should see an output of the read only role ARN that is needed to complete the AWS Linked Account in the New Relic Console. Copy the ARN and return to the https://one.newrelic.com/ console. Navigate to the "Infrastructure" module and select the "AWS" tab. In the top right corner of the screen, select "+ Add an AWS Account" and choose the "Use metric streams" option. 

Click the "Next" button at the bottom of the screen until you reach Step 5: Add Account Details. Provide an AWS Account Name that matches the same name (and naming standard) of the API Key you created. This should be: program - account level - app (i.e. ccdi-nonprod-mtp). Then, paste the IAM role arn copied to your clipboard (received from the terraform outputs) and paste it in the field labeled "Paste the ARN created in the previous step". 

### 6. Confirm Metric Reception
It may take up to 20 minutes for metrics to begin displaying in the New Relic platform. Return to the Infrastructure page and observe the summary metrics for the new account you just linked under the "AWS" tab. 


## Usage Examples
Please note that the following are just examples. The example values provided for the access keys, external IDs, etc. are fictitious. 

### Minimum Configuration 
<pre><code>module "new_relic_metric_pipeline" {
  source = "github.com/CBIIT/datacommons-devops/terraform/modules/firehose-metrics/"

  account_id                = data.aws_caller_identity.current.account_id
  app                       = var.app #i.e. "icdc"
# http_endpoint_access_key  = var.http_endpoint_access_key (do not store this value in GitHub. Instead, pass this value in when running Terraform Apply operations)
  level                     = var.level #i.e. "non-prod"
# new_relic_account_id      = var.new_relic_account_id (do not store this value in GitHub. Instead, pass this value in when running Terraform Apply operations)
  permission_boundary_arn   = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser"
  program                   = var.program #i.e. "crdc"
  s3_bucket_arn             = var.failed_metric_delivery_bucket #i.e "arn:aws:s3:::example-icdc-destination-bucket"
}</code></pre>


<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
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
| <a name="input_http_endpoint_url"></a> [http\_endpoint\_url](#input\_http\_endpoint\_url) | The HTTP endpoint URL to which Kinesis Firehose sends your data | `string` | `"https://aws-api.newrelic.com/cloudwatch-metrics/v1"` | no |
| <a name="input_iam_prefix"></a> [iam\_prefix](#input\_iam\_prefix) | The string prefix for IAM resource name attributes | `string` | `"power-user"` | no |
| <a name="input_include_filter"></a> [include\_filter](#input\_include\_filter) | Specify the service namespaces to include in metric stream in a list | `set(string)` | <pre>[<br>  "AWS/ES",<br>  "AWS/ApplicationELB",<br>  "AWS/ECS"<br>]</pre> | no |
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

| Name | Description |
|------|-------------|
| <a name="output_read_only_role_arn"></a> [read\_only\_role\_arn](#output\_read\_only\_role\_arn) | The ARN to copy/paste when creating a New Relic Linked Account |
<!-- END_TF_DOCS -->
