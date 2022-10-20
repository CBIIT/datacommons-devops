variable "app" {
  type        = string
  description = "The name of the application (i.e. 'mtp')"
}

variable "program" {
  type        = string
  description = "The name of the program (i.e. 'ccdi')"
}

variable "iam_prefix" {
  type        = string
  description = "The string prefix for IAM resource name attributes"
  default     = "power-user"
}

variable "level" {
  type        = string
  description = "The account level - either 'nonprod' or 'prod' are accepted"
}

variable "force_detach_policies" {
  type        = bool
  description = "Force detaching any policies the role has before destroying it"
  default     = false
}

variable "new_relic_account_id" {
  type        = string
  description = "The account provided by New Relic during the account link registration process"
  sensitive   = true
}

variable "new_relic_external_id" {
  type        = string
  description = "The external ID provided by New Relic during the account link registration process"
  sensitive   = true
}

variable "permission_boundary_arn" {
  type        = string
  description = "The arn of the permission boundary associated with the role"
}

variable "set_external_id_condition" {
  type = bool 
  description = "Set to true to use New Relic's external ID as a condition in the assume role policy"
}
