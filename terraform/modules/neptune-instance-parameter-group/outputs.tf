output "arn" {
  value       = aws_neptune_parameter_group.this.arn
  description = "the neptune instance parameter group arn"
  sensitive   = false
}

output "family" {
  value       = aws_neptune_parameter_group.this.family
  description = "the neptune instance parameter group family"
  sensitive   = false
}

output "name" {
  value       = aws_neptune_parameter_group.this.name
  description = "the neptune instance parameter group name"
  sensitive   = false
}

output "id" {
  value       = aws_neptune_parameter_group.this.id
  description = "the neptune instance parameter group id"
  sensitive   = false
}