output "application_fqdn" {
  value = aws_route53_record.dns_record.fqdn
}
output "application_dns_name" {
  value = aws_route53_record.dns_record.name
}