resource "aws_cloudwatch_metric_stream" "cw_stream" {
  name          = "${var.program}-${var.app}-${var.level}-cloudwatch-metric-stream"
  role_arn      = var.role_arn
  output_format = var.output_format
  firehose_arn  = var.firehose_delivery_stream_arn

  dynamic "include_filter" {
    for_each = var.include_filter

    content {
      namespace = include_filter.value
    }
  }
}
