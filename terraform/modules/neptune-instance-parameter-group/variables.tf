variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "enable_caching" {
  type        = bool
  description = "enable neptune query caching"
  default     = false
  sensitive   = false
}

variable "family" {
  type        = string
  description = "the neptune parameter group family"
  default     = "neptune1.2"
  sensitive   = false
}

variable "query_timeout" {
  type        = string
  description = "the timeout for neptune queries"
  default     = "120,000"
  sensitive   = false
}
