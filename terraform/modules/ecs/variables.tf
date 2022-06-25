variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}
variable "stack_name" {
  description = "name of the project"
  type        = string
}

variable "ecs_subnet_ids" {
  description = "Provide list private subnets to use in this VPC. Example 10.0.10.0/24,10.0.11.0/24"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC Id to to launch the ALB"
  type        = string
}

variable "ecs_launch_type" {
  description = "ecs launch type - FARGATE or EC2"
  type        = string
  default     = "FARGATE"
}

variable "ecs_scheduling_strategy" {
  description = "ecs scheduling strategy"
  type        = string
  default     = "REPLICA"
}

variable "ecs_network_mode" {
  description = "ecs network mode - bridge,host,awsvpc"
  type        = string
  default     = "awsvpc"
}

variable "alb_target_type" {
  type        = string
  description = "type of alb target - ip , instance, lambda"
  default     = "ip"
}

variable "application_url" {
  description = "url of the application"
  type        = string
}

variable "env" {
  description = "name of the environment to provision"
  type        = string
}

variable "microservices" {
  type = map(object({
    name                      = string
    port                      = number
    health_check_path         = string
    priority_rule_number      = number
    image_url                 = string
    cpu                       = number
    memory                    = number
    path                      = string
    number_container_replicas = number
  }))
}

variable "alb_https_listener_arn" {
  description = "alb https listener arn"
  type        = string
}

variable "ecs_security_group_ids" {
  description = "list of security groups to apply to this ecs"
  type        = list(string)
}
variable "ecs_task_role_arn" {
  description = "ecs task iam role arn"
  type        = string
}
variable "ecs_execution_role_arn" {
  description = "ecs execution iam role arn"
  type        = string
}

variable "ecs_execute_command_logging" {
  description = "The log setting to use for redirecting logs for ecs execute command results. Valid values are NONE, DEFAULT, and OVERRIDE."
  type        = string
  default     = "OVERRIDE"
}