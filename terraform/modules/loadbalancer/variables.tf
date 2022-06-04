variable "tags" {
  description = "tags to associate with this instance"
  type = map(string)
}
variable "stack_name" {
  description = "name of the project"
  type = string
}
variable "region" {
  description = "aws region to deploy"
  type = string
  default = "us-east-1"
}
variable "alb_name" {
  description = "Name for the ALB"
  type = string
  default = "alb"
}
variable "lb_type" {
  description = "Type of loadbalancer"
  type = string
  default = "application"
}
variable "internal_alb" {
  description = "is this alb internal?"
  default = false
  type = bool
}

variable "ssl_policy" {
  description = "specify ssl policy to use"
  default = "ELBSecurityPolicy-2016-08"
  type = string
}

variable "default_message" {
  description = "default message response from alb when resource is not available"
  default = "The requested resource is not found"
}
variable "vpc_id" {
  description = "VPC Id to to launch the ALB"
  type        = string
}

variable "certificate_domain_name" {
  description = "domain name for the ssl cert"
  type = string
}

variable "env" {
  description = "name of the environment to provision"
  type = string
}
variable "alb_subnet_ids" {
  description = "list of subnets to use for the alb"
  type = list(string)
}

variable "alb_security_group_ids" {
  description = "list of alb security groups"
  type = list(string)
}

variable "alb_log_bucket_name" {
  description = "s3"
  type = string
}

variable "acm_certificate_issued_type" {
  description = "specify the issue type of the acm certificate, allowed values are AMAZON_ISSUED & IMPORTED"
  type = string
  default = "AMAZON_ISSUED"
}