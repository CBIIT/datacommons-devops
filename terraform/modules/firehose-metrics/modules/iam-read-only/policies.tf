data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = [var.new_relic_account_id]
    }
    condition {
      test     = var.set_external_id_condition ? "StringEquals" : null
      variable = var.set_external_id_condition ? "sts:ExternalId" : null
      values   = var.set_external_id_condition ? [var.new_relic_external_id] : null
    }
  }
}
