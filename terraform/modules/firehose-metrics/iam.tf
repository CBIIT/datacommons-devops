resource "aws_iam_role" "cw_stream_to_firehose" {
  name                  = "${var.iam_prefix}-${var.program}-${var.app}-${var.level}-cloudwatch-stream-to-firehose"
  description           = "Allows CloudWatch Streams to send metric streams to Kinesis Data Firehose Delivery Streams"
  force_detach_policies = var.role_force_detach_policies
  assume_role_policy    = data.aws_iam_policy_document.cw_stream_to_firehose_assume_role.json
  permissions_boundary  = local.permissions_boundary_arn
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

######

resource "aws_iam_role" "kinesis" {
  name                  = "${var.iam_prefix}-${var.program}-${var.app}-${var.level}-kinesis-delivery"
  description           = "Allows kenisis delivery streams to delivery failed messages to S3"
  force_detach_policies = false
  assume_role_policy    = data.aws_iam_policy_document.kinesis_assume_role.json
  permissions_boundary  = local.permission_boundary_arn
}

resource "aws_iam_policy" "kinesis" {
  name        = "${var.iam_prefix}-${var.program}-${var.app}-${var.level}-kinesis-delivery"
  description = "Allows kenisis delivery streams to delivery failed messages to S3"
  policy      = data.aws_iam_policy_document.kenisis.json
}

resource "aws_iam_role_policy_attachment" "kinesis" {
  role       = aws_iam_role.kinesis.name
  policy_arn = aws_iam_policy.kinesis.arn
}