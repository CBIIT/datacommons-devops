variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}
variable "stack_name" {
  description = "name of the project"
  type        = string
}

variable "iam_prefix" {
  description = "The string prefix for IAM roles and policies to conform to NCI power-user compliance"
  type        = string
  default     = "power-user"
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
    path                      = list(string)
    number_container_replicas = number
  }))
}

variable "alb_https_listener_arn" {
  description = "alb https listener arn"
  type        = string
}

variable "ecs_execute_command_logging" {
  description = "The log setting to use for redirecting logs for ecs execute command results. Valid values are NONE, DEFAULT, and OVERRIDE."
  type        = string
  default     = "OVERRIDE"
}

variable "container_insights_setting" {
  description = "Whether or not the ECS cluster enables CloudWatch Container Insights"
  type        = string
  default     = "disabled"
}

variable "target_account_cloudone"{
  description = "to add check conditions on whether the resources are brought up in cloudone or not"
  type        = bool
  default = yes
}

variable "add_opensearch_permission" {
  type = bool
  default = false
  description = "choose to create opensearch permission or not"
}
variable "allow_cloudwatch_stream" {
  type = bool
  default = false
  description = "allow cloudwatch stream for the containers"

}
variable "domain_name" {
  type = string
  description = "domain name of this app"
  default = "bento-tools.org"
}

variable "create_neo4j_db" {
  type = bool
  default = false
  description = "choose to add neo4j container or not"
}
variable "central_ecr_account_id" {
  type = string
  description = "central ecr account number"
  default = null
}
variable "use_custom_trust_policy" {
  type = bool
  description = "use custom role trust policy"
  default = false
}

variable "custom_trust_policy" {
  type = string
  description = "custom role trust policy"
  default = null
}