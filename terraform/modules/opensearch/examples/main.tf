terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.19.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "opensearch" {
  source = "github.com/CBIIT/datacommons-devops/terraform/modules/opensearch"

  app             = var.app
  data_node_count = var.opensearch_data_node_count
  ebs_enabled     = var.opensearch_ebs_enabled
  ebs_volume_size = var.opensearch_ebs_volume_size
  engine_version  = var.opensearch_engine_version
  iam_prefix      = var.iam_prefix
  instance_type   = var.opensearch_instance_type
  log_retention   = var.opensearch_log_retention
  log_type        = var.opensearch_log_type
  multi-az        = var.opensearch_multi_az
  snapshot_hour   = var.opensearch_snapshot_hour
  subnet_ids      = ["subnet-12345678", "subnet-23456789"]
  tier            = "example"
  vpc_id          = "vpc-12345678"

}

variable "app" {
  type        = string
  description = "The name of the application for which this stack defines"
  default = "example"
}

variable "opensearch_data_node_count" {
  type        = number
  description = "The number of data nodes to provision for each instance in the cluster"
  default     = 2
}

variable "opensearch_ebs_enabled" {
  type        = bool
  description = "Set to true to enable EBS volume storage for the OpenSearch data nodes. Must select an EBS-compatible instance class."
  default     = true
}

variable "opensearch_ebs_volume_size" {
  type        = number
  description = "The size of the EBS volumes regarding disk space to allocate for the data nodes (GiB)"
  default     = 80
}

variable "opensearch_engine_version" {
  type        = string
  description = "The version of the OpenSearch engine (i.e. OpenSearch_1.2)"
  default     = "OpenSearch_1.2"
}

variable "iam_prefix" {
  type        = string
  description = "The policy and role prefix required by NCI PowerUser policy conditions"
  default     = "power-user"
}

variable "opensearch_instance_type" {
  type        = string
  description = "The class or type of the OpenSearch instance (i.e. t3.medium.search)"
  default     = "t3.medium.search"
}

variable "opensearch_log_retention" {
  type        = number
  description = "The number of days to retain logs sourced from the OpenSearch cluster"
  default     = 90
}

variable "opensearch_log_type" {
  type        = string
  description = "The type of OpenSearch logs to forward to CloudWatch"
  default     = "INDEX_SLOW_LOGS"
}

variable "opensearch_multi_az" {
  type        = bool
  description = "Set to true to enable a multi-az deployment of OpenSearch"
  default     = true
}

variable "opensearch_snapshot_hour" {
  type        = number
  description = "The time of day when the OpenSearch cluster will perform automated snapshots"
  default     = 23
}





