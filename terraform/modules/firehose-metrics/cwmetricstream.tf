resource "aws_cloudwatch_metric_stream" "cw_stream" {
  name          = "${var.program}-${var.app}-${var.level}-cloudwatch-metric-stream"
  role_arn      = aws_iam_role.cw_stream_to_firehose.arn
  output_format = var.output_format
  firehose_arn  = aws_kinesis_firehose_delivery_stream.kinesis.arn

  dynamic "include_filter" {
    for_each = var.include_filter
    content {
      namespace = each.value
    }
  }
}
