variable "sns_topic_name" {
  description = "The name of the SNS topic"
  type        = string
}

variable "slack_webhook_url" {
  description = "Slack webhook URL for notifications"
  type        = string
}

variable "resource_prefix" {
  description = "A prefix for naming resources"
  type        = string
}

variable "sns_display_name" {
  description = "Display name for SNS topic"
  type        = string
  default     = "DefaultDisplayName"
}
