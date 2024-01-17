variable "resource_prefix" {
  description = "Prefix for all resources"
   type        = string
}

variable "ecs_cluster_name" {
  description = "Name of the existing ECS cluster"
  type        = string
}

variable "ecs_task_definition" {
  description = "ARN of the existing ECS task definition"
  type        = string
}

variable "slack_notification_endpoint" {
  description = "Slack notification endpoint"
  type        = string
}

variable "cron_expression" {
  description = "Cron expression for the CloudWatch event rule"
   type        = string
}

variable "launch_type" {
  description = "ecs launch type - FARGATE or EC2"
  type        = string
  default     = "FARGATE"
}
