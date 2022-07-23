variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}

variable "ecr_repo_names" {
  description = "list of repo names"
  type        = list(string)
}

variable "stack_name" {
  description = "name of the project"
  type        = string
}

variable "env" {
  description = "name of the environment to provision"
  type        = string
}

variable "create_env_specific_repo" {
  description = "choose to create environment specific repo. Example bento-dev-frontend"
  type = bool
  default = true
}