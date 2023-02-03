
variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}

variable "destination_bucket_name" {
  description = "destination bucket name"
  type = string
  default = ""
}

variable "create_destination_bucket" {
  type = bool
  default = false
  description = "choose to create destination bucket"
}
variable "replication_role_arn" {
  description = "replication role arn"
  type = string
}
