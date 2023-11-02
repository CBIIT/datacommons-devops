output "address" {
  value       = aws_db_instance.this.address
  description = "address of the instance"
  sensitive   = false
}

output "arn" {
  value       = aws_db_instance.this.arn
  description = "arn of the instance"
  sensitive   = false
}

output "availability_zone" {
  value       = aws_db_instance.this.availability_zone
  description = "availability zone of the instance"
  sensitive   = false
}

output "db_name" {
  value       = aws_db_instance.this.db_name
  description = "name of the database"
  sensitive   = false
}

output "db_subnet_group_name" {
  value       = aws_db_instance.this.db_subnet_group_name
  description = "name of the subnet group"
  sensitive   = false
}

output "domain" {
  value       = aws_db_instance.this.domain
  description = "domain of the instance"
  sensitive   = false
}

output "endpoint" {
  value       = aws_db_instance.this.endpoint
  description = "endpoint of the instance"
  sensitive   = false
}

output "hosted_zone_id" {
  value       = aws_db_instance.this.hosted_zone_id
  description = "hosted zone id of the instance"
  sensitive   = false
}

output "id" {
  value       = aws_db_instance.this.id
  description = "id of the instance"
  sensitive   = false
}

output "identifier" {
  value       = aws_db_instance.this.identifier
  description = "identifier of the instance"
  sensitive   = false
}

output "identifier_prefix" {
  value       = aws_db_instance.this.identifier_prefix
  description = "identifier prefix of the instance"
  sensitive   = false
}

output "monitoring_role_arn" {
  value       = aws_db_instance.this.monitoring_role_arn
  description = "monitoring role arn of the instance"
  sensitive   = false
}

output "password" {
  value       = aws_db_instance.this.password
  description = "password of the instance"
  sensitive   = true
}

output "port" {
  value       = aws_db_instance.this.port
  description = "port of the instance"
  sensitive   = false
}

output "resource_id" {
  value       = aws_db_instance.this.resource_id
  description = "resource id of the instance"
  sensitive   = false
}

output "security_group_arn" {
  value       = aws_security_group.this[0].arn
  description = "arn of the security group - if create_security_group is true"
  sensitive   = false
}

output "security_group_id" {
  value       = aws_security_group.this[0].id
  description = "id of the security group - if create_security_group is true"
  sensitive   = false
}

output "security_group_name" {
  value       = aws_security_group.this[0].name
  description = "name of the security group - if create_security_group is true"
  sensitive   = false
}

output "username" {
  value       = aws_db_instance.this.username
  description = "username of the instance"
  sensitive   = false
}