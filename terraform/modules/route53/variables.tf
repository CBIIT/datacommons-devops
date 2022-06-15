variable "domain_name" {
  description = "domain name for the application"
  type        = string
}
variable "application_subdomain" {
  description = "subdomain of the app"
  type        = string
}
variable "alb_dns_name" {
  description = "alb dns name"
  type        = string
}

variable "alb_zone_id" {
  description = "alb dns name"
  type        = string
}
variable "env" {
  description = "name of the environment to provision"
  type        = string
}
