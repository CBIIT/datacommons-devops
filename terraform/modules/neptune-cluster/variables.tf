variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "allow_major_version_upgrade" {
  type        = string
  description = "indicates that major version upgrades are allowed"
  default     = false
  sensitive   = false
}

variable "apply_immediately" {
  type        = string
  description = "indicates whether the changes should be applied immediately or during the next maintenance window"
  default     = true
  sensitive   = false
}

variable "auto_minor_version_upgrade" {
  type        = bool
  description = "indicates that minor engine upgrades are applied automatically to the instance during the maintenance window"
  default     = true
  sensitive   = false
}

variable "backup_retention_period" {
  type        = string
  description = "number of days to retain backups for"
  default     = 1
  sensitive   = false
}

variable "copy_tags_to_snapshot" {
  type        = bool
  description = "whether to copy tags to snapshots"
  default     = true
  sensitive   = false
}

variable "create_parameter_groups" {
  type        = bool
  description = "whether to create parameter groups for the cluster and instance(s)"
  default     = false
  sensitive   = false
}

variable "database_subnet_ids" {
  type        = set(string)
  description = "the list of subnet IDs to associate with the cluster"
  sensitive   = false
}

variable "deletion_protection" {
  type        = bool
  description = "whether to enable deletion protection"
  default     = true
  sensitive   = false
}

variable "enable_caching" {
  type        = bool
  description = "whether to enable caching for the cluster"
  default     = false
  sensitive   = false
}

variable "enable_cloudwatch_logs_exports" {
  type        = list(string)
  description = "list of log types to export to cloudwatch"
  default     = ["audit"]
  sensitive   = false
}

variable "enable_serverless" {
  type        = bool
  description = "whether to enable serverless mode for the cluster"
  default     = true
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
  description = "the version of the database engine to use"
  default     = "1.2.1.0"
  sensitive   = false
}

variable "final_snapshot_identifier" {
  type        = string
  description = "the name of the final snapshot to be created immediately before deleting the cluster"
  default     = null
  sensitive   = false
}

variable "iam_roles" {
  type        = set(string)
  description = "the list of IAM roles to associate with the cluster"
  default     = []
  sensitive   = false
}

variable "iam_database_authentication_enabled" {
  type        = bool
  description = "whether to enable IAM database authentication for the cluster"
  default     = false
  sensitive   = false
}

variable "instance_class" {
  type        = string
  description = "the instance class to use (i.e., db.r5.large) - only required when serverless is not enabled"
  default     = "db.r5.large"
  sensitive   = false
}

variable "max_capacity" {
  type        = number
  description = "the maximum capacity for the cluster in neptune capacity units when serverless is enabled"
  default     = 128
  sensitive   = false
}

variable "min_capacity" {
  type        = number
  description = "the minimum capacity for the cluster in neptune capacity units when serverless is enabled"
  default     = 2
  sensitive   = false
}

variable "preferred_backup_window" {
  type        = string
  description = "the daily time range during which automated backups are created if automated backups are enabled"
  default     = "02:00-04:00"
  sensitive   = false
}

variable "preferred_maintenance_window" {
  type        = string
  description = "the weekly time range during which system maintenance can occur, in (UTC)"
  default     = "sun:05:00-sun:09:00"
  sensitive   = false
}

variable "port" {
  type        = number
  description = "the port on which the DB accepts connections"
  default     = 8182
  sensitive   = false
}

variable "query_timeout" {
  type        = string
  description = "time in milliseconds that a query can run before it is terminated by the cluster"
  default     = "120000"
  sensitive   = false
}

variable "replication_source_identifier" {
  type        = string
  description = "the ARN of the source Neptune instance if this Neptune instance is a read replica"
  default     = null
  sensitive   = false
}

variable "skip_final_snapshot" {
  type        = bool
  description = "whether to skip the creation of a final snapshot before deleting the cluster"
  default     = true
  sensitive   = false
}

variable "snapshot_identifier" {
  type        = string
  description = "the name of an existing snapshot from which to create this cluster"
  default     = null
  sensitive   = false
}

variable "vpc_security_group_ids" {
  type        = set(string)
  description = "the list of security group IDs to associate with the cluster"
  sensitive   = false
}