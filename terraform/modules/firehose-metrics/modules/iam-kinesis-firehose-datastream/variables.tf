##########################################################################################
######  Required Variables ###############################################################
##########################################################################################
variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "account_id" {
  type        = string
  description = "The ID of the target account (use data.aws_caller_identity.current.account_id)"
}

variable "app" {
  type        = string
  description = "The name of the application (i.e. 'mtp')"
}

variable "level" {
  type        = string
  description = "The account level - either 'nonprod' or 'prod' are accepted"
}

variable "permission_boundary_arn" {
  type        = string
  description = "The arn of the permission boundaries for roles. Set to null for prod account levels"
}

variable "program" {
  type        = string
  description = "The name of the program (i.e. 'ccdi')"
}

variable "s3_bucket_arn" {
  type        = string
  description = "The arn of the S3 bucket where failed message deliveries to New Relic are delivered"
}

##########################################################################################
######  Optional Variables ###############################################################
##########################################################################################

variable "force_detach_policies" {
  type        = bool
  description = "Set to true to automatically detach policies when deleting a role"
  default     = false
}

variable "iam_prefix" {
  type        = string
  description = "The string prefix for IAM resource name attributes"
  default     = "power-user"
}
