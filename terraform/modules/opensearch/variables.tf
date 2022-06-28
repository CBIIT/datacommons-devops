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

variable "opensearch_tls_policy" {
  description = "Provide the TLS policy to associate with the OpenSearch domain to enforce HTTPS communications"
  type        = string
  default     = "Policy-Min-TLS-1-2-2019-07"
}

variable "opensearch_log_types" {
  description = "List of log types that OpenSearch forwards to CloudWatch. Options include INDEX_SLOW_LOGS, SEARCH_SLOW_LOGS, ES_APPLICATION_LOGS, AUDIT_LOGS"
  type        = list(string)
  default     = ["AUDIT_LOGS"]
}

variable "opensearch_autotune_state" {
  description = "Tell OpenSearch to enable or disable autotuning. Options include ENABLED and DISABLED"
  value       = string
  default     = "ENABLED"
}

variable "opensearch_autotune_rollback_type" {
  description = "Tell OpenSearch how to respond to disabling AutoTune. Options include NO_ROLLBACK and DEFAULT_ROLLBACK"
  type        = string
  default     = "DEFAULT_ROLLBACK"
}