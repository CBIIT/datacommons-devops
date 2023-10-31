output "arn" {
  value       = aws_neptune_cluster_parameter_group.this.arn
  description = "arn of the neptune cluster parameter group"
  sensitive   = false
}

output "family" {
  value       = aws_neptune_cluster_parameter_group.this.family
  description = "family of the neptune cluster parameter group"
  sensitive   = false
}

output "name" {
  value       = aws_neptune_cluster_parameter_group.this.name
  description = "name of the neptune cluster parameter group"
  sensitive   = false
}

output "id" {
  value       = aws_neptune_cluster_parameter_group.this.id
  description = "id of the neptune cluster parameter group"
  sensitive   = false
}