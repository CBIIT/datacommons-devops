locals {
  account_arn = format("arn:aws:iam::%s:root", data.aws_caller_identity.current.account_id)

  # Access Policies
  local      = var.access_scheme == "local" ? data.aws_iam_policy_document.local.json : ""
  standard   = var.access_scheme == "standard" ? data.aws_iam_policy_document.standard.json : ""
  alternate  = var.access_scheme == "alternate" ? data.aws_iam_policy_document.alternate.json : ""
  policy_doc = coalesce(local.local, local.standard, local.alternate)
}