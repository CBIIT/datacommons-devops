output "arn" {
  value       = aws_opensearch_domain.this.arn
  description = "The ARN of the OpenSearch domain"
  sensitive   = false
}

output "dashboard_endpoint" {
  value       = aws_opensearch_domain.this.dashboard_endpoint
  description = "The endpoint of the OpenSearch domain dashboard"
  sensitive   = false
}

output "domain_id" {
  value       = aws_opensearch_domain.this.domain_id
  description = "The unique identifier for the OpenSearch domain"
  sensitive   = false
}

output "domain_name" {
  value       = aws_opensearch_domain.this.domain_name
  description = "The name of the OpenSearch domain"
  sensitive   = false
}

output "endpoint" {
  value       = aws_opensearch_domain.this.endpoint
  description = "The domain-specific endpoint used to submit index, search, and data upload requests to an OpenSearch domain"
  sensitive   = false
}

output "id" {
  value       = aws_opensearch_domain.this.id
  description = "The unique identifier for the OpenSearch domain"
  sensitive   = false
}

output "security_group_arn" {
  value       = local.outputs.security_group_arn
  description = "The ARN of the security group for the OpenSearch domain"
  sensitive   = false
}

output "security_group_id" {
  value       = local.outputs.security_group_id
  description = "The ID of the security group for the OpenSearch domain"
  sensitive   = false
}

output "role_arn" {
  value       = local.outputs.role_arn
  description = "The ARN of the IAM role used to take snapshots of the OpenSearch domain"
  sensitive   = false
}

output "role_id" {
  value       = local.outputs.role_id
  description = "The ID of the IAM role used to take snapshots of the OpenSearch domain"
  sensitive   = false
}

output "role_name" {
  value       = local.outputs.role_name
  description = "The name of the IAM role used to take snapshots of the OpenSearch domain"
  sensitive   = false
}