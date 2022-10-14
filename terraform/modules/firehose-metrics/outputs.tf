output "cw-metric-stream-arn" {
  value = aws_cloudwatch_metric_stream.cw_stream.arn
}

output "cw-metric-stream-output_format" {
  value = aws_cloudwatch_metric_stream.cw_stream.output_format
}

output "cw-metric-stream-name" {
  value = aws_cloudwatch_metric_stream.cw_stream.name
}

output "kinesis_arn" {
  value = aws_kinesis_firehose_delivery_stream.kinesis.arn
}