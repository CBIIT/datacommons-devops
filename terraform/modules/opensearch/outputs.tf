output "opensearch_endpoint" {
  value = aws_opensearch_domain.es.endpoint
}

output "opensearch_arn" {
  value = aws_opensearch_domain.es.arn
}

output "opensearch_cloudwatch_log_group_arn" {
  value = aws_cloudwatch_log_group.es.arn
}