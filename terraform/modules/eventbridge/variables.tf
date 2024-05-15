variable "eventbridge_name" {
  description = "Name of the EventBridge rule"
  type        = string
}

variable "schedule_expression" {
  description = "Schedule expression for the EventBridge rule"
  type        = string
}

variable "target_type" {
  description = "Type of the EventBridge target (e.g., 'ecs-task', 'lambda', 'sns')"
  type        = string
}

variable "target_arn" {
  description = "ARN of the EventBridge target"
  type        = string
}

variable "ecs_cluster_arn" {
  description = "ARN of the ECS cluster for ECS task type targets"
  type        = string
  default     = ""
}

variable "task_definition_arn" {
  description = "ARN of the ECS task definition for ECS task type targets"
  type        = string
  default     = ""
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for ECS task type targets"
  type        = list(string)
  default     = []
}

variable "ecs_security_groups" {
  description = "List of security group IDs for ECS task type targets"
  type        = list(string)
  default     = []
}

variable "assign_public_ip" {
  description = "Whether to assign a public IP to the ECS task. Valid values: 'ENABLED', 'DISABLED'"
  type        = string
  default     = "DISABLED"
}

/*variable "input" {
  description = "Input passed to the target, must be JSON"
  type        = string
  default     = "{}"
}

variable "input_paths" {
  description = "JSON paths to be extracted from the event and used in the input template"
  type        = map(string)
  default     = {}
}*/

variable "resource_prefix" {
  description = "The prefix to add when creating resources"
  type        = string
}

variable "iam_prefix" {
  description = "The string prefix for IAM roles and policies to conform to NCI power-user compliance"
  type        = string
  default     = "power-user"
}

variable "target_account_cloudone"{
  description = "to add check conditions on whether the resources are brought up in cloudone or not"
  type        = bool
  default     = true
}
