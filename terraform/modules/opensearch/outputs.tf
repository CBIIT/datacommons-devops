output "opensearch_endpoint" {
  value = aws_opensearch_domain.es.endpoint
  description = "the opensearch domain endpoint url"
}

output "opensearch_arn" {
  value = aws_opensearch_domain.es.arn
  description = "the OpenSearch domain arn"
}

output "opensearch_cloudwatch_log_group_arn" {
  value = aws_cloudwatch_log_group.es.arn
  description = "the log group arn that collects OpenSearch logs"
}