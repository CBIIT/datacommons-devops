variable "iam_prefix" {
  description = "The string prefix for IAM roles and policies to conform to NCI power-user compliance"
  type        = string
  default     = "power-user"
}

variable "target_account_cloudone"{
  description = "to add check conditions on whether the resources are brought up in cloudone or not"
  type        = bool
  default = false
}
variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}
variable "stack_name" {
  description = "name of the project"
  type        = string
}
variable "env" {
  description = "name of the environment to provision"
  type        = string
}
variable "source_bucket_name" {
  description = "source bucket name"
  type = string
  default = ""
}
variable "destination_bucket_name" {
  description = "destination bucket name"
  type = string
  default = ""
}
variable "create_source_bucket" {
  type = bool
  default = false
  description = "choose to create source bucket"
}
variable "replication_destination_account_id" {
  type = string
  description = "replication account id"
  default = ""
}
variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}
