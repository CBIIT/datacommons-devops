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

variable "apply_immediately" {
  type        = bool
  description = "specifies whether any instance modifications are applied immediately, or during the next maintenance window"
  default     = true
  sensitive   = false
}

variable "auto_minor_version_upgrade" {
  type        = bool
  description = "indicates that minor engine upgrades are applied automatically to the instance during the maintenance window"
  default     = true
  sensitive   = false
}

variable "availability_zone" {
  type        = string
  description = "the Availability Zone where the instance will be created"
  default     = null
  sensitive   = false
}

variable "cluster_identifier" {
  type        = string
  description = "the name of the neptune cluster"
  default     = null
  sensitive   = false
}

variable "engine" {
  type        = string
  description = "the name of the database engine to be used for this instance"
  default     = "neptune"
  sensitive   = false
}

variable "engine_version" {
  type        = string
  description = "the version number of the database engine to use"
  default     = null
  sensitive   = false
}

variable "instance_class" {
  type        = string
  description = "the instance class to use"
  default     = "db.serverless"
  sensitive   = false
}

variable "neptune_subnet_group_name" {
  type        = string
  description = "the name of the neptune subnet group"
  default     = null
  sensitive   = false
}

variable "neptune_parameter_group_name" {
  type        = string
  description = "the name of the neptune parameter group"
  default     = null
  sensitive   = false
}

variable "port" {
  type        = number
  description = "the port on which the DB accepts connections"
  default     = null
  sensitive   = false
}

variable "promotion_tier" {
  type        = number
  description = "a value that specifies the order in which an instance is promoted to the primary instance after a failure of the existing primary instance"
  default     = null
  sensitive   = false
}

variable "publicly_accessible"{
  type        = bool
  description = "if its publicly accessible or not"
  default     = false
  sensitive   = false
}