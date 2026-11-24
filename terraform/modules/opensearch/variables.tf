variable "access_policies" {
  type        = string
  description = "Required if create_access_policies is false. Provide json output from IAM Policy Document"
  default     = null
  sensitive   = false
}

variable "attach_permissions_boundary" {
  type        = bool
  description = "Whether to attach the permissions boundary to the OpenSearch Snapshot Role"
  default     = false
  sensitive   = false
}

variable "auto_software_update_enabled" {
  type        = bool
  description = "Whether automatic service software updates are enabled for the domain"
  default     = false
  sensitive   = false
}

variable "auto_tune_enabled" {
  type        = bool
  description = "Whether to enable the OpenSearch Auto-Tune feature"
  default     = true
  sensitive   = false
}

variable "automated_snapshot_start_hour" {
  type        = number
  description = "hour when automated snapshot to be taken"
  default     = 5
  sensitive   = false
}

variable "cluster_tshirt_size" {
  type        = string
  description = "Select a T-Shirt size for the cluster"
  default     = "xs"
  sensitive   = false
  validation {
    condition     = contains(["xs", "sm", "md", "lg", "xl"], var.cluster_tshirt_size)
    error_message = "The variable cluster_tshirt_size must be one of: xs, sm, md, lg, xl"
  }
}

variable "cold_storage_enabled" {
  type        = bool
  description = "Boolean to enable cold storage for an OpenSearch domain. Master and ultrawarm nodes must be enabled for cold storage."
  default     = false
  sensitive   = false
}

variable "create_access_policies" {
  type        = bool
  description = "Whether to allow the module to create the access policies for the OpenSearch domain"
  default     = true
  sensitive   = false
}

variable "create_cloudwatch_log_policy" {
  type        = bool
  description = "Whether to allow the module to create the cloudwatch log policy for the OpenSearch domain"
  default     = true
  sensitive   = false
}

variable "create_security_group" {
  type        = bool
  description = "Whether to allow the module to create the security group for the OpenSearch domain"
  default     = true
  sensitive   = false
}

variable "create_snapshot_role" {
  type        = bool
  description = "Whether to allow the module to create the snapshot role for the OpenSearch domain"
  default     = true
  sensitive   = false
}

variable "dedicated_master_count" {
  type        = number
  description = "The number of Dedicated Master nodes in the cluster"
  default     = null
  sensitive   = false
}

variable "dedicated_master_enabled" {
  type        = bool
  description = "Whether to enable Dedicated Master nodes in the cluster"
  default     = false
  sensitive   = false
}

variable "dedicated_master_type" {
  type        = string
  description = "The instance type of the Dedicated Master nodes in the cluster"
  default     = null
  sensitive   = false
}

variable "encrypt_at_rest" {
  type        = bool
  description = "Whether to enable encryption at rest for the domain"
  default     = true
  sensitive   = false
}

variable "enforce_https" {
  type        = bool
  description = "Whether to require HTTPS for all traffic to the domain"
  default     = true
  sensitive   = false
}

variable "engine_version" {
  type        = string
  description = "The engine version of the OpenSearch domain (i.e., OpenSearch_2.11)"
  sensitive   = false
}

variable "iam_prefix" {
  type        = string
  description = "Prefix for IAM resource names"
  default     = "power-user"
  sensitive   = false
}

variable "instance_count" {
  type        = number
  description = "The number of Data Nodes attached to the cluster in each availability zone"
  default     = null
  sensitive   = false
}

variable "instance_type" {
  type        = string
  description = "The instance type of the Data Nodes in the cluster"
  default     = null
  sensitive   = false
}

variable "log_retention_in_days" {
  type        = number
  description = "The number of days to retain OpenSearch logs in CloudWatch Logs"
  default     = 180
  sensitive   = false
}

variable "log_types" {
  type        = set(string)
  description = "The type of OpenSearch logs that will be published to CloudWatch Logs"
  default     = ["INDEX_SLOW_LOGS", "SEARCH_SLOW_LOGS", "ES_APPLICATION_LOGS"]
  sensitive   = false
}

variable "resource_prefix" {
  type        = string
  description = "Prefix for resource names, advised to use the program-tier-app convention"
  sensitive   = false
}

variable "s3_snapshot_bucket_arn" {
  type        = string
  description = "The ARN of the S3 bucket to store OpenSearch snapshots"
  default     = null
  sensitive   = false
}

variable "security_group_ids" {
  type        = set(string)
  description = "A set of one or more Security Group IDs to associate with the cluster"
  default     = []
  sensitive   = false
}

variable "subnet_ids" {
  type        = set(string)
  description = "A set of one or more Private Subnet IDs to associate with the cluster"
  sensitive   = false
}

variable "tags" {
  type        = map(string)
  description = "tags to associate with this instance"
  default     = {}
  sensitive   = false
}

variable "tls_security_policy" {
  type        = string
  description = "The name of the TLS security policy to apply to the domain"
  default     = "Policy-Min-TLS-1-2-PFS-2023-10"
  sensitive   = false
}

variable "volume_size" {
  type        = number
  description = "The size of the EBS volumes attached to data nodes (in GB) - between 10 and 200"
  default     = null
  sensitive   = false
}

variable "volume_type" {
  type        = string
  description = "The volume type to use for data and master nodes"
  default     = "gp3"
  sensitive   = false
}

variable "vpc_id" {
  type        = string
  description = "the ID of the VPC the OpenSearch cluster is being deployed into"
  sensitive   = false
}

variable "warm_count" {
  type        = number
  description = "The total number of warm nodes attached to the cluster"
  default     = null
  sensitive   = false
}

variable "warm_enabled" {
  type        = bool
  description = "Whether to enable warm nodes in the cluster"
  default     = false
  sensitive   = false
}

variable "warm_type" {
  type        = string
  description = "The instance type of the warm nodes in the cluster"
  default     = null
  sensitive   = false
}

variable "zone_awareness_enabled" {
  type        = bool
  description = "Whether to enable Multi-AZ cluster deployment"
  default     = false
  sensitive   = false
}
