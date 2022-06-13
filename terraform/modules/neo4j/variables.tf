variable "ebs_volume_type" {
  description = "EVS volume type"
  default = "standard"
  type = string
}

variable "ssh_user" {
  type = string
  description = "name of the ec2 user"
  default = "bento"
}
variable "db_instance_volume_size" {
  description = "volume size of the instances"
  type = number
  default = 100
}
variable "vpc_id" {
  description = "vpc id to to launch the ALB"
  type        = string
}
variable "database_name" {
  description = "name of the database"
  type = string
  default = "neo4j"
}
variable "database_instance_type" {
  description = "ec2 instance type to use"
  type = string
  default = "t3.medium"
}
variable "database_password" {
  description = "set database password"
  type = string
  default = "custodian"
}
variable "db_private_ip" {
  description = "private ip of the db instance"
  type = string
}
variable "ssh_key_name" {
  description = "name of the ssh key to manage the instances"
  type = string
  default = "devops"
}
variable "tags" {
  description = "tags to associate with this instance"
  type = map(string)
}
variable "stack_name" {
  description = "name of the project"
  type = string
}

variable "iam_instance_profile_name" {
  description = "name of iam_instance_profile to apply to this instance"
  type = string
  default = "bento-dev-ecs-instance-profile"
}
variable "db_subnet_id" {
  description = "subnet id to launch db"
  type = string
}
variable "db_security_group_ids" {
  description = "security group id for the db"
  type = list(string)
}
variable "env" {
  description = "name of the environment to provision"
  type = string
}
variable "public_ssh_key_ssm_parameter_name" {
  description = "name of the ssm parameter holding ssh key content"
  default = "ssh_public_key"
  type = string
}