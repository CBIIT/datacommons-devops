# Security group outputs
output "efs_security_group_id" {
  value = aws_security_group.efs.id
}