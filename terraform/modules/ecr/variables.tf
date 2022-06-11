variable "tags" {
  description = "tags to associate with this instance"
  type = map(string)
}

variable "ecr_repo_names" {
  description = "list of repo names"
  type = list(string)
}

variable "stack_name" {
  description = "name of the project"
  type = string
}

variable "env" {
  description = "name of the environment to provision"
  type = string
}