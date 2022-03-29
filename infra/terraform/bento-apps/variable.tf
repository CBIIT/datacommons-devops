variable "stack_name" {
  description = "name of the project"
  type = string
}
variable "tags" {
  description = "tags to associate with this instance"
  type = map(string)
}

variable "vpc_id" {
  description = "VPC Id to to launch the ALB"
  type        = string
}

variable "region" {
  description = "aws region to deploy"
  type = string
  default = "us-east-1"
}
variable "profile" {
  description = "iam user profile to use"
  type = string
  default = "default"
}
variable "public_subnet_ids" {
  description = "Provide list of public subnets to use in this VPC. Example 10.0.1.0/24,10.0.2.0/24"
  default     = []
  type = list(string)
}

variable "private_subnet_ids" {
  description = "Provide list private subnets to use in this VPC. Example 10.0.10.0/24,10.0.11.0/24"
  default     = []
  type = list(string)
}

variable "allowed_subnet_ip_block" {
  description = "subnet ip block"
  type = list(string)
}

variable "domain_name" {
  description = "domain name for the application"
  type = string
}

variable "app_sub_domain" {
  description = "url of the app"
  type = string
  default = null
}


variable "microservices" {
  type = map(object({
    name = string
    port = number
    health_check_path = string
    priority_rule_number = number
    image_url = string
    cpu = number
    memory = number
    path = string
  }))
}
variable "certificate_domain_name" {
  description = "domain name for the ssl cert"
  type = string
}

variable "elasticsearch_instance_type" {
  description = "type of instance to be used to create the elasticsearch cluster"
  type = string
  default = "t3.medium.elasticsearch"
}

variable "elasticsearch_version" {
  type = string
  description = "specify es version"
  default = "1.1"
}
