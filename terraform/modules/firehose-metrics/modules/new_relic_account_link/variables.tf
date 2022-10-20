##########################################################################################
######  Required Variables ###############################################################
##########################################################################################

variable "account_id" {
  type        = string
  description = "The AWS Account ID that the IAM role was provisioned to"
}
variable "app" {
  type        = string
  description = "The name of the application (i.e. 'mtp')"
}

variable "level" {
  type        = string
  description = "The account level - either 'nonprod' or 'prod' are accepted"
}

variable "new_relic_account_id" {
  type        = string
  description = "The Leidos New Relic account id. If omitted, will default to account_id specified in the provider"
  sensitive   = true
}

variable "new_relic_iam_readonly_role" {
  type        = string
  description = "The read only role that New Relic assumes to enrich metrics"
}

variable "program" {
  type        = string
  description = "The name of the program (i.e. 'ccdi')"
}

##########################################################################################
######  Optional Variables ###############################################################
##########################################################################################

variable "iam_prefix" {
  type        = string
  description = "The prefix used for all IAM resources created in Cloud One"
  default     = "power-user"
}

variable "new_relic_ingest_type" {
  type        = string
  description = "Valid options are BROWSER or LICENSE"
  default     = "LICENSE"
}

variable "new_relic_key_type" {
  type        = string
  description = "The type of API Key to create. Can be INGEST or USER"
  default     = "INGEST"
}

variable "new_relic_metric_collection_mode" {
  type        = string
  description = "How New Relic receives metrics from source - either PUSH or PULL"
  default     = "PUSH"
}
