variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}
variable "tags" {
  description = "tags to associate with this instance"
  type = map(string)
}
variable "stack_name" {
  description = "name of the project"
  type = string
}
variable "domain_name" {
  description = "domain name for the application"
  type = string
}
variable "env" {
  description = "environment"
  type = string
}

variable "cloudfront_distribution_bucket_name" {
  description = "specify the name of s3 bucket for cloudfront"
  type = string
}

variable "alarms" {
  description = "alarms to be configured"
  type = map(map(string))
}

variable "slack_secret_name" {
  type = string
  description = "name of cloudfront slack secret"
}
variable "cloudfront_slack_channel_name" {
  type = string
  description = "cloudfront slack name"
}

variable "iam_prefix" {
  description = "The string prefix for IAM roles and policies to conform to NCI power-user compliance"
  type        = string
  default     = "power-user"
}

variable "target_account_cloudone"{
  description = "to add check conditions on whether the resources are brought up in cloudone or not"
  type        = bool
  default     =  false
}
variable "slack_url_secret_key" {
  description = "secret key name for the slack url"
  type = string
  default = "cloud-front-slack-url"
}
variable "create_files_bucket" {
  description = "indicate if you want to create files bucket or use existing one"
  type = bool
  default = false
}

variable "public_key_path" {
  description = "path of public key"
  default = null
}