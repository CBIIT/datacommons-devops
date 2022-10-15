##########################################################################################
######  Required Variables ###############################################################
##########################################################################################

variable "app" {
  type        = string
  description = "The name of the application (i.e. 'mtp')"
}

variable "firehose_delivery_stream_arn" {
  type = string 
  description = "The arn of the kinesis firehose delivery stream to push metrics to"
}

variable "level" {
  type        = string
  description = "The account level - either 'nonprod' or 'prod' are accepted"
}

variable "program" {
  type        = string
  description = "The name of the program (i.e. 'ccdi')"
}

variable "role_arn" {
  type        = string
  description = "The arn of the role for cloudwatch metric stream to assume"
}

##########################################################################################
######  Optional Variables ###############################################################
##########################################################################################

variable "include_filter" {
  type        = set(string)
  description = "Specify the service namespaces to include in metric stream in a list"
  default     = ["AWS/ES", "AWS/ApplicationELB"]
}

variable "output_format" {
  type        = string
  description = "Output format of the CloudWatch Metric Stream - can be json or opentelemetry0.7"
  default     = "opentelemetry0.7"
}


