output "arn" {
  value = aws_kinesis_firehose_delivery_stream.kinesis.arn
}

output "id" {
  value = aws_kinesis_firehose_delivery_stream.kinesis.id
}

output "destination" {
  value = aws_kinesis_firehose_delivery_stream.kinesis.destination
}