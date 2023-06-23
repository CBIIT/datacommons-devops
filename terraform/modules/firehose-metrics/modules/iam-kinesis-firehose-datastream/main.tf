resource "aws_iam_role" "kinesis" {
  name                  = "${var.iam_prefix}-${var.resource_prefix}-kinesis-delivery"
  description           = "Allows kenisis delivery streams to delivery failed messages to S3"
  force_detach_policies = var.force_detach_policies
  assume_role_policy    = data.aws_iam_policy_document.kinesis_assume_role.json
  permissions_boundary  = var.permission_boundary_arn
}

resource "aws_iam_policy" "kinesis" {
  name        = "${var.iam_prefix}-${var.resource_prefix}-kinesis-delivery"
  description = "Allows kenisis delivery streams to delivery failed messages to S3"
  policy      = data.aws_iam_policy_document.kenisis.json
}

resource "aws_iam_role_policy_attachment" "kinesis" {
  role       = aws_iam_role.kinesis.name
  policy_arn = aws_iam_policy.kinesis.arn
}
