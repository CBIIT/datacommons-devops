data "aws_iam_policy_document" "events_assume_role" {
  count = var.target_type != "" ? 1 : 0
  statement {
  effect  = "Allow"
  actions = ["sts:AssumeRole"]

  principals {
    type        = "Service"
    identifiers = ["events.amazonaws.com"]
  }
}
}
