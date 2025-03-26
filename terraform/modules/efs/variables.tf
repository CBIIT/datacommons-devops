variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}

variable "project" {
  description = "name of the project"
  type        = string
}

variable "efs_subnet_ids" {
  description = "Provide list private subnets to use in this VPC. Example 10.0.10.0/24,10.0.11.0/24"
  type        = list(string)
}

variable "vpc_id" {
  description = "VPC Id to to launch the ALB"
  type        = string
}

variable "env" {
  description = "name of the environment to provision"
  type        = string
}