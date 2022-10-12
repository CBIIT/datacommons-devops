resource "aws_cloudwatch_metric_stream" "cw_stream" {
  name          = "${var.program}-${var.app}-${var.level}-cloudwatch-metric-stream"
  role_arn      = aws_iam_role.cw_stream_to_firehose.arn
  output_format = var.output_format
  firehose_arn  = var.firehose_delivery_stream_arn

  dynamic "include_filter" {
    for_each = var.include_filter
    content {
      namespace = include_filter.value
    }
  }
}

resource "aws_iam_role" "cw_stream_to_firehose" {
  name                  = "${var.iam_prefix}-${var.program}-${var.app}-${var.level}-cloudwatch-stream-to-firehose"
  description           = "Allows CloudWatch Streams to send metric streams to Kinesis Data Firehose Delivery Streams"
  force_detach_policies = var.role_force_detach_policies
  assume_role_policy    = data.aws_iam_policy_document.cw_stream_to_firehose_assume_role.json
  permissions_boundary  = local.permission_boundary_arn
}

resource "aws_iam_role_policy_attachment" "cw_stream_to_firehose" {
  role       = aws_iam_role.cw_stream_to_firehose.name
  policy_arn = aws_iam_policy.cw_stream_to_firehose.arn
}

resource "aws_iam_policy" "cw_stream_to_firehose" {
  name        = "${var.iam_prefix}-${var.program}-${var.app}-${var.level}-cloudwatch-stream-to-firehose"
  description = "Allows CloudWatch Streams to send metric streams to Kinesis Data Firehose Delivery Streams"
  policy      = data.aws_iam_policy_document.cw_stream_to_firehose.json
}