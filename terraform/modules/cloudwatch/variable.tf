variable "resource_prefix" {
  description = "Prefix for all resources"
  type        = string
}

variable "cron_expression" {
  description = "Cron expression for the CloudWatch event rule"
  type        = string
}

variable "target_type" {
  description = "Select a target type for the CloudWatch event"
  type        = string
  default     = ""
}

variable "custom_target_arn" {
  description = "ARN for the custom target"
  type        = string
  default     = ""
}
