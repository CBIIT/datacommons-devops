variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "tags" {
  description = "tags to associate with this instance"
  type = map(string)
}

variable "deletion_protection" {
  description = "prevent deletion"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "number of days to keep backup"
  type        = number
  default     = 35
}

variable "neptune_engine_version" {
  description = "aurora database engine version."
  type        = string
  default     = "1.2.0.1"
}

variable "neptune_iam_roles" {
  description = "A List of ARNs for the IAM roles to associate to the Neptune Cluster."
  type        = list(string)
  default     = []
}

variable "create_neptune_subnet_group" {
  type        = bool
  description = "whether to create a neptune subnet group for the rds instance"
  default     = true
  sensitive   = false
}

variable "db_subnet_group_name" {
  type        = string
  description = "name of the db subnet group - required if create_db_subnet_group is false"
  default     = null
  sensitive   = false
}

variable "backup_window" {
  type        = string
  description = "the backup window for the rds instance in UTC time"
  default     = "02:00-03:00"
  sensitive   = false
}

variable "maintenance_window" {
  type        = string
  description = "the maintenance window for the rds instance in UTC time"
  default     = "Sun:05:00-Sun:07:00"
  sensitive   = false
}

variable "skip_final_snapshot" {
  description = "specify snapshot if snapshot should be created on cluster destroy."
  type        = bool
  default     = false
}

variable "storage_encrypted" {
  description = "Enable underlying storage encryption."
  type        = bool
  default     = true
}

variable "kms_key_arn" {
  description = "The ARN for the KMS encryption key"
  type        = string
}

variable "create_neptune_security_group" {
  type        = bool
  description = "whether to create a security group for the neptune cluster"
  default     = true
  sensitive   = false
}
variable "tags" {
  description = "tags to associate with this instance"
  type = map(string)
}

variable "apply_immediately" {
  type        = bool
  description = "whether or not to apply changes immediately"
  default     = true
  sensitive   = false
}

variable "neptune_instance_class" {
  type        = string
  description = "instance class to use for the neptune instance"
  sensitive   = false
  default     = "db.serverless"
}

variable "subnet_ids" {
  type        = list(string)
  description = "list of subnet ids to associate with the neptune instance - necessary if create_db_subnet_group is true"
  default     = []
  sensitive   = false
}

variable "vpc_id" {
  type        = string
  description = "id of the vpc to create the neptune instance in"
  sensitive   = false
}

