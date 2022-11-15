variable "app" {
  description = "name of the app"
  type        = string
}
variable "region" {
  description = "aws region to use for this resource"
  type = string
  default = "us-east-1"
}

variable "neo4j_user" {
  type        = string
  description = "neo4j user"
  default     = "neo4j"
}
variable "neo4j_password" {
  type        = string
  description = "neo4j password"
}
variable "neo4j_ip" {
  type        = string
  description = "name or IP address of the db instance for this tier"
}

variable "mysql_user" {
  type        = string
  description = "mysql user"
  default     = ""
}
variable "mysql_password" {
  type        = string
  description = "mysql password"
  default     = ""
}
variable "mysql_database" {
  type        = string
  description = "mysql database"
  default     = ""
}
variable "mysql_host" {
  type        = string
  description = "mysql host"
  default     = ""
}
variable "cookie_secret" {
  type        = string
  description = "cookie secret"
  default     = ""
}

variable "es_host" {
  type        = string
  description = "opensearch enpoint for this tier"
}
variable "indexd_url" {
  type        = string
  description = "indexd url"
}

variable "sumo_collector_endpoint" {
  type        = string
  description = "endpoint for Sumo collectors"
  default     = "collectors.fed.sumologic.com"
}
variable "sumo_collector_token_frontend" {
  type        = string
  description = "Sumo collector token for frontend"
}
variable "sumo_collector_token_backend" {
  type        = string
  description = "Sumo collector token for backend"
}
variable "sumo_collector_token_files" {
  type        = string
  description = "Sumo collector token for files"
  default     = ""
}
variable "sumo_collector_token_users" {
  type        = string
  description = "Sumo collector token for users"
  default     = ""
}
variable "sumo_collector_token_auth" {
  type        = string
  description = "Sumo collector token for auth"
  default     = ""
}

variable "github_token" {
  type        = string
  description = "github token"
  sensitive   = true
  default     = ""
}