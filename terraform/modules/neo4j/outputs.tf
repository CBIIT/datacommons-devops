output "private_ip" {
  value = aws_instance.db.private_ip
}
output "db_security_group_id" {
  value = var.create_security_group ? aws_security_group.database_sg[0].id : data.aws_security_group.sg[0].id
}
output "db_security_group_arn" {
  value = var.create_security_group ? aws_security_group.database_sg[0].arn : data.aws_security_group.sg[0].arn
}