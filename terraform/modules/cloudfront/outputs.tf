output "cloudfront_distribution_endpoint" {
  value = aws_cloudfront_distribution.bento_distribution.domain_name
}