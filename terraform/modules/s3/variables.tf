variable "tags" {
  description = "tags to associate with this resource"
  type = map(string)
}
variable "bucket_name" {
  description = "name of the s3 bucket"
  type = string
}
variable "enable_version" {
  description = "enable bucket versioning"
  default = false
  type = bool
}
variable "lifecycle_rule" {
  description = "object lifecycle rule"
  type = any
  default = []
}
variable "bucket_acl" {
  description = "type of bucket acl to apply"
  type = string
  default = "private"
}
variable "bucket_policy" {
  description = "s3 bucket policy"
  type = any
  default = []
}
variable "attach_bucket_policy" {
  description = "set to true if you want bucket policy and provide value for policy variable"
  type        = bool
  default     = false
}
variable "force_destroy_bucket" {
  description = "force destroy s3 bucket."
  type = bool
  default = false
}