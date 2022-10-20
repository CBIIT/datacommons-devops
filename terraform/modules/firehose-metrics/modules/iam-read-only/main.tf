resource "aws_iam_role" "read_only" {
  name                  = "${var.iam_prefix}-${var.program}-${var.app}-${var.level}-newrelic-read-only"
  description           = "Allow config details to be collected to enrich metric observability"
  force_detach_policies = var.force_detach_policies
  assume_role_policy    = data.aws_iam_policy_document.assume_role.json
  permissions_boundary  = var.permission_boundary_arn
}

resource "aws_iam_role_policy_attachment" "read_only" {
  role       = aws_iam_role.read_only.name
  policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}
