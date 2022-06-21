variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}

variable "stack_name" {
  description = "name of the project"
  type        = string
}

variable "vpc_id" {
  description = "the ID of the VPC the OpenSearch cluster is being deployed into"
  type        = string
}

variable "opensearch_instance_type" {
  description = "type of instance to be used to create the OpenSearch cluster"
  type        = string
  default     = "t3.medium.search"
}

variable "opensearch_version" {
  type        = string
  description = "specify es version"
  default     = "OpenSearch_1.2"
}

variable "create_os_service_role" {
  type        = bool
  default     = false
  description = "change this value to true if running this script for the first time"
}

variable "opensearch_subnet_ids" {
  description = "list of subnet ids to use"
  type        = list(string)
}

variable "env" {
  description = "name of the environment to provision"
  type        = string
}

variable "automated_snapshot_start_hour" {
  description = "hour when automated snapshot to be taken"
  type        = number
  default     = 23
}

variable "opensearch_ebs_volume_size" {
  description = "size of the ebs volume attached to the opensearch instance"
  type        = number
  default     = 30
}

variable "opensearch_instance_count" {
  description = "the number of data nodes to provision for each instance in the cluster"
  type        = number
  default     = 2
}

variable "multi_az_enabled" {
  description = "set to true to enable multi-az deployment"
  type        = bool
}

variable "opensearch_log_type" {
  description = "type of opensearch logs to send to cloudwatch (INDEX_SLOW_LOGS, SEARCH_SLOW_LOGS, AUDIT_LOGS, ES_APPLICATION_LOGS)"
  type        = string
  default     = "INDEX_SLOW_LOGS"
}

variable "opensearch_logs_enabled" {
  description = "set to true to enable OpenSearch to forward logs to CloudWatch"
  type        = bool
  default     = true
}

variable "opensearch_autotune_desired_state" {
  description = "Auto-Tune desired state for the domain - options are 'ENABLED' or 'DISABLED'"
  type        = string
  default     = "ENABLED"
}

variable "opensearch_rollback_on_autotune_disable" {
  description = "Whether to roll back to default Auto-Tune settings when disabling Auto-Tune - options are 'DEFAULT_ROLLBACK' or 'NO_ROLLBACK'"
  type        = string
  default     = "DEFAULT_ROLLBACK"
}

