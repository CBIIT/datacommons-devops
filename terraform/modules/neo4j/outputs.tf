output "private_ip" {
  value = aws_instance.db.private_ip
}
output "db_security_group_id" {
  value = aws_security_group.database_sg.id
}
output "db_security_group_arn" {
  value = aws_security_group.database_sg.arn
}