resource "aws_kinesis_firehose_delivery_stream" "kinesis" {
  name        = "${var.program}-${var.app}-${var.level}-kinesis-firehose-stream"
  destination = var.destination

  http_endpoint_configuration {
    url                = var.http_endpoint_url
    name               = var.http_endpoint_name
    access_key         = var.http_endpoint_access_key
    buffering_size     = var.buffer_size
    buffering_interval = var.buffer_interval
    role_arn           = var.role_arn
    s3_backup_mode     = var.s3_backup_mode

    request_configuration {
      content_encoding = var.content_encoding
    }
  }

  s3_configuration {
    role_arn            = var.role_arn
    bucket_arn          = var.s3_bucket_arn
    prefix              = var.s3_object_prefix
    error_output_prefix = var.s3_error_output_prefix
    buffer_size         = var.buffer_size
    buffer_interval     = var.buffer_interval
    compression_format  = var.s3_compression_format
  }
}


