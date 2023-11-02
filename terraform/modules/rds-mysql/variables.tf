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
variable "allocated_storage" {
  type        = number
  description = "allocated storage in gibibytes - minimum is 100"
  default     = 100
  sensitive   = false
}

variable "allow_major_version_upgrade" {
  type        = bool
  description = "allow major version upgrade"
  default     = false
  sensitive   = false
}

variable "apply_immediately" {
  type        = bool
  description = "whether to apply changes immediately or wait until next maintenance window"
  default     = true
  sensitive   = false
}

variable "attach_permissions_boundary" {
  type        = bool
  description = "whether to attach a permissions boundary to the role - required if enable_enhanced_monitoring is true"
  default     = null
  sensitive   = false
}

variable "auto_minor_version_upgrade" {
  type        = bool
  description = "whether minor database modifications are automatically applied during maintenance windows"
  default     = true
  sensitive   = false
}

variable "backup_retention_period" {
  type        = number
  description = "backup retention period in days - between 0 and 35"
  default     = 7
  sensitive   = false
}

variable "backup_window" {
  type        = string
  description = "backup window in UTC - format hh24:mi-hh24:mi"
  default     = "02:00-04:00"
  sensitive   = false
}

variable "create_db_subnet_group" {
  type        = bool
  description = "whether to create a db subnet group"
  default     = true
  sensitive   = false
}

variable "create_from_snapshot" {
  type        = bool
  description = "whether to create the instance from a snapshot - if true, provide shapshot id for snapshot_identifier variable"
  default     = false
  sensitive   = false
}

variable "create_security_group" {
  type        = bool
  description = "Whether to create a security group for the rds instance"
  default     = true
  sensitive   = false
}

variable "db_name" {
  type        = string
  description = "name of the database within RDS to create"
  sensitive   = false
}

variable "db_subnet_group_name" {
  type        = string
  description = "name of the db subnet group - required if create_db_subnet_group is false"
  default     = null
  sensitive   = false
}

variable "deletion_protection" {
  type        = bool
  description = "whether to enable deletion protection"
  default     = true
  sensitive   = false
}

variable "enable_enhanced_monitoring" {
  type        = bool
  description = "whether to enable enhanced monitoring"
  default     = true
  sensitive   = false
}

variable "enabled_cloudwatch_logs_exports" {
  type        = list(string)
  description = "list of log types to export to cloudwatch"
  default     = ["audit", "error", "general", "slowquery"]
  sensitive   = false
}

variable "engine" {
  type        = string
  description = "database engine to use"
  default     = "mysql"
  sensitive   = false
}

variable "engine_version" {
  type        = string
  description = "database engine version to use - if auto_minor_version_upgrade is true, no need to specify patch version"
  default     = "8.0"
  sensitive   = false
}

variable "iam_database_authentication_enabled" {
  type        = bool
  description = "whether to enable iam database authentication"
  default     = false
  sensitive   = false
}

variable "instance_class" {
  type        = string
  description = "rds instance class to use"
  default     = "db.t3.medium"
  sensitive   = false
}

variable "iops" {
  type        = number
  description = "iops to associate with the instance - only valid for 'io1' and 'gp3' storage types"
  default     = 3000
  sensitive   = false
}

variable "maintenance_window" {
  type        = string
  description = "maintenance window in UTC - format ddd:hh24:mi-ddd:hh24:mi"
  default     = "sun:20:00-sun:23:00"
  sensitive   = false
}

variable "monitoring_interval" {
  type        = number
  description = "interval in seconds to monitor the instance - 0 to disable, otherwise 1, 5, 10, 15, 30 , and 60 are valid"
  default     = 10
  sensitive   = false
}

variable "multi_az" {
  type        = bool
  description = "whether to create a multi-az instance"
  default     = true
  sensitive   = false
}

variable "password" {
  type        = string
  description = "password for the database"
  sensitive   = true
}

variable "performance_insights_enabled" {
  type        = bool
  description = "whether to enable performance insights"
  default     = true
  sensitive   = false
}

variable "performance_insights_retention_period" {
  type        = number
  description = "performance insights retention period in days - between 7 and 731 with a multiple of 31"
  default     = 7
  sensitive   = false
}

variable "rds_suffix" {
  type        = string
  description = "suffix to append to the rds instance name"
  default     = "rds"
  sensitive   = false
}

variable "snapshot_identifier" {
  type        = string
  description = "snapshot identifier to use for the instance - required if create_from_snapshot is true"
  default     = null
  sensitive   = false
}

variable "storage_throughput" {
  type        = number
  description = "storage throughput in gibibytes per second - only valid for 'gp3' storage type"
  default     = 125
  sensitive   = false
}

variable "storage_type" {
  type        = string
  description = "type of ebs block storage to associate with the instance - either 'standard', 'gp2', 'gp3', or 'io1'"
  default     = "gp3"
  sensitive   = false
}

variable "subnet_ids" {
  type        = list(string)
  description = "list of subnet ids to place the instance in - required if create_db_subnet_group is true"
  default     = []
  sensitive   = false
}

variable "tags" {
  type        = map(string)
  description = "map of tags to apply to the instance"
  default     = {}
  sensitive   = false
}

variable "username" {
  type        = string
  description = "username for the database"
  sensitive   = false
}

variable "vpc_security_group_ids" {
  type        = list(string)
  description = "list of security group ids to associate with the instance - required if create_security_group is false"
  default     = []
  sensitive   = false
}

variable "vpc_id" {
  type        = string
  description = "id of the vpc to create the security group in - required if create_security_group is true"
  default     = null
  sensitive   = false
}