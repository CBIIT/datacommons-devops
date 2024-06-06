resource "aws_iam_role" "events_role" {
  count = var.target_type != "" ? 1 : 0
  name  = "${var.resource_prefix}-cloudwatch-events-role"

  assume_role_policy = data.aws_iam_policy_document.events_assume_role[0].json
}

resource "aws_iam_role_policy_attachment" "events_attachment" {
  count      = var.target_type != "" ? 1 : 0
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.events_role[0].name
}
