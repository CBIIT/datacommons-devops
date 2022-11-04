output "opensearch_endpoint" {
  value       = aws_opensearch_domain.os_domain.endpoint
  description = "the opensearch domain endpoint url"
}

output "opensearch_arn" {
  value       = aws_opensearch_domain.os_domain.arn
  description = "the OpenSearch domain arn"
}

output "opensearch_cloudwatch_log_group_arn" {
  value       = aws_cloudwatch_log_group.os_logs.arn
  description = "the log group arn that collects OpenSearch logs"
}

output "opensearch_security_group_id" {
  value       = aws_security_group.os_sg.id
  description = "the id of the security group associated with the OpenSearch cluster"
}

output "opensearch_security_group_arn" {
  value       = aws_security_group.os_sg.arn
  description = "the arn of the security group associated with the OpenSearch cluster"
}