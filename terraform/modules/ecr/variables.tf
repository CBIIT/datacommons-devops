variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}

variable "ecr_repo_names" {
  description = "list of repo names"
  type        = list(string)
}

variable "project" {
  description = "the name of the project"
  type        = string
}

variable "env" {
  description = "name of the environment to provision"
  type        = string
}

# Lifecycle Policy Configuration
variable "max_images_to_keep" {
  description = "the maximum number of images to keep in the repository"
  type = number
  default = 20
}

# Replication
variable "replication_destination_registry_id" {
  type = string
  description = "registry id for destination image"
  default = ""
}

variable "replication_source_registry_id" {
  type = string
  description = "registry id for source image"
  default = ""
}

variable "enable_ecr_replication" {
  description = "enable ecr replication"
  type = bool
  default = false
}

variable "allow_ecr_replication" {
  description = "allow ecr replication"
  type = bool
  default = false
}