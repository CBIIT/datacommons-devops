output "api_key" {
  value = newrelic_api_access_key.this.key
}

output "external_id" {
  value = newrelic_cloud_aws_link_account.this.id
}