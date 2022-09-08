############################################################################################################
############  Required Variables  ##########################################################################
############################################################################################################

variable "account_id" {
  type        = string
  description = "Account ID for the deployment target - use 'data.aws_caller_identity.current.account_id'"
}

variable "app" {
  type        = string
  description = "The name of the application (i.e. 'mtp')"
}

variable "external_id" {
  type        = string
  description = "The endpoint external id for the delivery stream trust policy condition"
}

variable "http_endpoint_access_key" {
  type        = string
  description = "The access key required for Kinesis Firehose to authenticate with the HTTP endpoint selected as the destination"
}

variable "level" {
  type        = string
  description = "The account level - either 'nonprod' or 'prod' are accepted"
}

variable "program" {
  type        = string
  description = "The name of the program (i.e. 'ccdi')"
}

variable "s3_bucket_arn" {
  type        = string
  description = "ARN of the bucket that serves as the destination for Kinesis delivery failures"
}

############################################################################################################
############  Optional Variables  ##########################################################################
############################################################################################################

variable "buffer_interval" {
  type        = number
  description = "Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination"
  default     = 60
}

variable "buffer_size" {
  type        = number
  description = "Buffer incoming data to the specified size, in MBs, before delivering it to the destination"
  default     = 1
}

variable "content_encoding" {
  type        = string
  description = "Kinesis Data Firehose uses the content encoding to compress the body of a request before sending the request to the destination - valid values are NONE and GZIP"
  default     = "GZIP"
}

variable "destination" {
  type        = string
  description = "the destination to where the data is delivered. The only options are 'extended_s3', 'redshift', 'elasticsearch', and 'http_endpoint'"
  default     = "http_endpoint"
}

variable "http_endpoint_name" {
  type        = string
  description = "The HTTP endpoint name"
  default     = "New Relic"
}

variable "http_endpoint_url" {
  type        = string
  description = "The HTTP endpoint URL to which Kinesis Firehose sends your data"
  default     = "https://aws-api.newrelic.com/cloudwatch-metrics/v1"
}

variable "iam_prefix" {
  type        = string
  description = "The string prefix for IAM resource name attributes"
  default     = "power-user"
}

variable "include_filter" {
  type        = set(string)
  description = "Specify the service namespaces to include in metric stream in a list"
  default     = ["AWS/ES", "AWS/ApplicationELB"]
}

variable "output_format" {
  type        = string
  description = "Output format of the CloudWatch Metric Stream - can be 'json' or 'opentelemetry0.7'"
  default     = "opentelemetry0.7"
}

variable "role_force_detach_policies" {
  type        = bool
  description = "Force detaching any policies the role has before destroying it"
  default     = false
}

variable "s3_backup_mode" {
  type        = string
  description = "Defines how documents should be delivered to Amazon S3. Valid values are 'FailedDataOnly' and 'AllData'"
  default     = "FailedDataOnly"
}

variable "s3_compression_format" {
  type        = string
  description = "File compression format - values are 'GZIP', 'ZIP', 'Snappy', & 'HADOOP_SNAPPY'"
  default     = "UNCOMPRESSED"
}

variable "s3_error_output_prefix" {
  type        = string
  description = "Prefix added to failed records before writing them to S3 - immediately follows bucket name"
  default     = null
}

variable "s3_object_prefix" {
  type        = string
  description = "The 'YYYY/MM/DD/HH' time format prefix is automatically used for delivered S3 files. You can specify an extra prefix to be added in front of the time format prefix"
  default     = null
}
