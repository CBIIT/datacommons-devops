variable "resource_prefix" {
  description = "the prefix to add when creating resources"
  type        = string
}

variable "service" {
  type        = string
  description = "Name of the service where the monitoring is configured. example ecs, database etc"
}

variable "program" {
  type        = string
  description = "Name of the program where the application is running. example ccdi or crdc etc"
}

variable "tags" {
  description = "tags to associate with this instance"
  type        = map(string)
}
variable "app" {
  description = "name of the app"
  type        = string
}
variable "sumologic_access_id" {
  type        = string
  description = "Sumo Logic Access ID"
}
variable "sumologic_access_key" {
  type        = string
  description = "Sumo Logic Access Key"
  sensitive   = true
}

variable "newrelic_account_id" {
  type        = string
  description = "New Relic Account ID"
}
variable "newrelic_api_key" {
  type        = string
  description = "New Relic API Key"
  sensitive   = true
}

variable "microservices" {
  type = map(object({
    name                      = string
    port                      = number
    health_check_path         = string
    priority_rule_number      = number
    image_url                 = string
    cpu                       = number
    memory                    = number
    path                      = list(string)
    number_container_replicas = number
  }))
}