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
