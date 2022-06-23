variable "bucket_name" {
  description = "name of the s3 bucket"
  type        = string
}
variable "s3_force_destroy" {
  description = "force destroy s3 bucket"
  type        = string
}

variable "tags" {
  description = "tags to associate with this resource"
  type        = map(string)
}

# variable "bucket_policy" {
#   description = "s3 bucket policy"
#   type        = any
#   default     = []
# }

variable "stack_name" {
  description = "name of the project"
  type        = string
}

variable "env" {
  description = "name of the environment to provision"
  type        = string
}