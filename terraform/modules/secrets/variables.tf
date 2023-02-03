variable "app" {
  description = "name of the app"
  type        = string
}
variable "region" {
  description = "aws region to use for this resource"
  type = string
  default = "us-east-1"
}

variable "secret_values" {
  type = map(object({
    secretKey = string
    secretValue = map(string)
    description = string
  }))
}