terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.19.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "example" {
  source = "github.com/CBIIT/datacommons-devops/terraform/modules/loadbalancer"

  stack_name          = "example"
  alb_type            = "application"
  alb_internal        = false
  ssl_policy          = var.ssl_policy
  default_message     = var.default_message
  vpc_id              = ""
  alb_certificate_arn = ""
  env                 = "dev"
  alb_subnet_ids      = var.alb_subnet_ids
  alb_log_bucket_name = var.alb_log_bucket_name
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

variable "ssl_policy" {
  description = "specify ssl policy to use"
  default     = "ELBSecurityPolicy-2016-08"
  type        = string
}

variable "default_message" {
  description = "default message response from alb when resource is not available"
  default     = "The requested resource is not found"
  type        = string
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
  default     = "project-log-bucket"
}
