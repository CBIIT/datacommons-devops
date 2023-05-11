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

variable "alb_type" {
  description = "Type of loadbalancer"
  type        = string
  default     = "application"
}

variable "alb_internal" {
  description = "is this alb internal?"
  default     = false
  type        = bool
}

variable "alb_ssl_policy" {
  description = "specify ssl policy to use"
  default     = "ELBSecurityPolicy-TLS-1-2-Ext-2018-06"
  type        = string
}

variable "alb_default_message" {
  description = "default message response from alb when resource is not available"
  default     = "The requested resource is not found"
}

variable "vpc_id" {
  description = "VPC Id to launch the ALB"
  type        = string
}

variable "alb_certificate_arn" {
  description = "arn for the ssl cert"
  type        = string
}

variable "env" {
  description = "name of the environment to provision"
  type        = string
}

variable "alb_subnet_ids" {
  description = "list of subnets to use for the alb"
  type        = list(string)
}

variable "alb_log_bucket_name" {
  description = "s3"
  type        = string
}

