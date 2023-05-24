resource "aws_iam_role" "cw_stream_to_firehose" {
  name                  = "${var.iam_prefix}-${var.resource_prefix}-cloudwatch-stream-to-firehose"
  description           = "Allows CloudWatch Streams to send metric streams to Kinesis Data Firehose Delivery Streams"
  force_detach_policies = var.force_detach_policies
  assume_role_policy    = data.aws_iam_policy_document.cw_stream_to_firehose_assume_role.json
  permissions_boundary  = var.permission_boundary_arn
}

resource "aws_iam_role_policy_attachment" "cw_stream_to_firehose" {
  role       = aws_iam_role.cw_stream_to_firehose.name
  policy_arn = aws_iam_policy.cw_stream_to_firehose.arn
}

resource "aws_iam_policy" "cw_stream_to_firehose" {
  name        = "${var.iam_prefix}-${var.resource_prefix}-cloudwatch-stream-to-firehose"
  description = "Allows CloudWatch Streams to send metric streams to Kinesis Data Firehose Delivery Streams"
  policy      = data.aws_iam_policy_document.cw_stream_to_firehose.json
}