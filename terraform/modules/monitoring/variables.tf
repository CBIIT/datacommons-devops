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
  description = "Newrelic Account ID"
  sensitive   = true
}
variable "newrelic_api_key" {
  type        = string
  description = "Newrelic API Key"
  sensitive   = true
}