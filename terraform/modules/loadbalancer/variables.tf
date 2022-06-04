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
variable "cloud_platform" {
  description = "choose platform to use"
  type = string
}

variable "s3_object_expiration_days" {
  description = "number of days for object to live"
  type = number
  default = 720
}
variable "s3_object_nonactive_expiration_days" {
  description = "number of days to retain non active objects"
  type = number
  default = 90
}
variable "s3_object_standard_ia_transition_days" {
  description = "number of days for an object to transition to standard_ia storage class"
  default = 120
  type = number
}
variable "s3_object_glacier_transition_days" {
  description = "number of days for an object to transition to glacier storage class"
  default = 180
  type = number
}

variable "create_alb" {
  description = "choose to create alb or not"
  type = bool
  default = true
}
variable "lb_type" {
  description = "Type of loadbalance"
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

variable "domain_name" {
  description = "domain name for the application"
  type = string
}

variable "public_subnet_ids" {
  description = "Provide list of public subnets to use in this VPC. Example 10.0.1.0/24,10.0.2.0/24"
  type = list(string)
}

variable "private_subnet_ids" {
  description = "Provide list private subnets to use in this VPC. Example 10.0.10.0/24,10.0.11.0/24"
  type = list(string)
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
variable "alb_allowed_ip_range" {
  description = "allowed subnet range for alb"
  type = list(string)
}
variable "alb_security_group_ids" {
  description = "list of alb security groups"
  type = list(string)
}

variable "alb_logs_bucket_name" {
  description = "s3"
  type = string
}

variable "acm_certificate_issue_type" {
  description = "specify the issue type of the acm certificate, allowed values are AMAZON_ISSUED & IMPORTED"
  type = string
  default = "AMAZON_ISSUED"
}