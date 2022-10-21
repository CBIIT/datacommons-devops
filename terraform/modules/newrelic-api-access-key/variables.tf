
variable "app" {
  type        = string
  description = "The name of the application (i.e. 'mtp')"
}

variable "level" {
  type        = string
  description = "The account level - either 'nonprod' or 'prod' are accepted"
}

variable "new_relic_account_id" {
  type        = number
  description = "The Leidos New Relic account id. If omitted, will default to account_id specified in the provider"
  sensitive   = true
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

variable "program" {
  type        = string
  description = "The name of the program (i.e. 'ccdi')"
}
