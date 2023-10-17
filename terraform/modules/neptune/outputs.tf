output "cluster_arn" {
  value       = aws_neptune_cluster.neptune_cluster.arn
  description = "arn of the neptune domain"
  sensitive   = false
}

output "cluster_resource_id" {
  value       = aws_neptune_cluster.neptune_cluster.cluster_resource_id
  description = "domain_id of the neptune domain"
  sensitive   = false
}

output "instance_arn" {
  value       = aws_neptune_cluster_instance.neptune_instance.arn
  description = "arn of the neptune instance"
  sensitive   = false
}

output "instance_endpoint" {
  value       = aws_neptune_cluster_instance.neptune_instance.endpoint
  description = "neptune instance endpoint"
  sensitive   = false
}

output "instance_id" {
  value       = aws_neptune_cluster_instance.neptune_instance.id
  description = "id of the neptune instance id"
  sensitive   = false
}

output "security_group_arn" {
  value       = aws_security_group.neptune[0].arn
  description = "arn of the security group if created by this module"
  sensitive   = false
}

output "security_group_id" {
  value       = aws_security_group.neptune[0].id
  description = "id of the security group if created by this module"
  sensitive   = false
}