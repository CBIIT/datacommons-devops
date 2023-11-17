output "address" {
  value       = aws_neptune_cluster_instance.this.address
  description = "The hostname of the instance. See also endpoint and port."
  sensitive   = false
}

output "arn" {
  value       = aws_neptune_cluster_instance.this.arn
  description = "The ARN of the neptune instance"
  sensitive   = false
}

output "cluster_identifier" {
  value       = aws_neptune_cluster_instance.this.cluster_identifier
  description = "The neptune cluster identifier"
  sensitive   = false
}

output "dbi_resource_id" {
  value       = aws_neptune_cluster_instance.this.dbi_resource_id
  description = "The neptune instance resource ID"
  sensitive   = false
}

output "endpoint" {
  value       = aws_neptune_cluster_instance.this.endpoint
  description = "The hostname of the instance. See also address and port."
  sensitive   = false
}

output "id" {
  value       = aws_neptune_cluster_instance.this.id
  description = "The neptune instance ID"
  sensitive   = false
}

output "identifier" {
  value       = aws_neptune_cluster_instance.this.identifier
  description = "The neptune instance identifier"
  sensitive   = false
}