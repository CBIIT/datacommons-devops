variable "custom_role_policy_arns" {
  description = "list of policy arns defined for this role"
  type = list(string)
  default = null
}
variable "trusted_role_arns" {
  description = "list of trusted roles arns"
  type = list(string)
  default = null
}
variable "iam_role_name" {
  description = "name of the role"
  type = string
}
variable "add_custom_policy" {
  description = "add other policies other than managed policy"
  type = bool
  default = false
}
variable "custom_policy_name" {
  description = "name of custom policy"
  type = string
  default = null
}
variable "iam_policy_description" {
  description = "description of iam policy"
  type = string
  default = null
}
variable "iam_policy" {
  description = "iam policy document"
  type = string
  default = null
}
variable "trusted_role_services" {
  default =  null
  description = "list of trusted service"
  type = list(string)
}