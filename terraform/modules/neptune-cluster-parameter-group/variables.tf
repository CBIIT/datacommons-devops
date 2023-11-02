variable "app" {
  type        = string
  description = "the name of the application expressed as an acronym"
  sensitive   = false
}

variable "env" {
  type        = string
  description = "the target tier ('dev', 'qa', 'stage', 'nonprod' or 'prod'.)"
  sensitive   = false

  validation {
    condition     = contains(["dev", "qa", "stage", "prod", "nonprod"], var.env)
    error_message = "valid values are 'dev', 'qa', 'stage', 'prod', and 'nonprod'"
  }
}

variable "program" {
  type        = string
  description = "the program associated with the application"
  sensitive   = false

  validation {
    condition     = contains(["crdc", "ccdi", "ctos", "fnl"], var.program)
    error_message = "valid values for program are 'crdc', 'ccdi', 'fnl' and 'ctos'"
  }
}

variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "enable_audit_log" {
  type        = bool
  description = "whether to enable audit logs"
  default     = true
  sensitive   = false
}

variable "family" {
  type        = string
  description = "the family of the neptune cluster parameter group"
  default     = "neptune1.2"
  sensitive   = false
}