resource "newrelic_cloud_aws_link_account" "this" {
  name                   = "${var.program}-${var.level}-${var.app}"
  account_id             = var.new_relic_account_id
  arn                    = "arn:aws:iam:${var.account_id}:role/${var.iam_prefix}-${var.level}-${var.app}-newrelic-role"
  metric_collection_mode = var.new_relic_metric_collection_mode
}
