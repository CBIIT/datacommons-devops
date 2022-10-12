##################################
#  Required Variables ############
##################################

variable "account_id" {
  type        = string
  description = "Account ID for the deployment target - use 'data.aws_caller_identity.current.account_id"
}

variable "app" {
  type        = string
  description = "The name of the application (i.e. 'mtp')"
}

variable "firehose_delivery_stream_arn" {
  type        = string
  description = "ARN of the Amazon Kinesis Firehose delivery stream to use for this metric stream"
}

variable "level" {
  type        = string
  description = "The account level - either 'nonprod' or 'prod' are accepted"
}

variable "program" {
  type        = string
  description = "The name of the program (i.e. 'ccdi')"
}

##################################
#  Optional Variables ############
##################################

variable "iam_prefix" {
  type        = string
  description = "The string prefix for IAM resource name attributes"
  default     = "power-user"
}

variable "include_filter" {
  type        = set(string)
  description = "Specify the service namespaces to include in metric stream in a list"
  default = [ "AWS/ES", "AWS/ApplicationELB" ]
}

variable "output_format" {
  type        = string
  description = "Output format of the CloudWatch Metric Stream - can be json or opentelemetry0.7"
  default     = "opentelemetry0.7"
}

variable "role_force_detach_policies" {
  type        = bool
  description = "Force detaching any policies the role has before destroying it"
  default     = false
}
