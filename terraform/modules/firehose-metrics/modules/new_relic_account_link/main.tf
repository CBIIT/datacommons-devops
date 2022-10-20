resource "newrelic_cloud_aws_link_account" "this" {
  name                   = "${var.program}-${var.level}-${var.app}"
  account_id             = var.new_relic_account_id
  arn                    = "arn:aws:iam:${account_id}:role/${var.iam_prefix}-${var.level}-${var.app}-newrelic-role"
  metric_collection_mode = var.new_relic_metric_collection_mode
}

resource "newrelic_api_access_key" "this" {
  account_id  = var.new_relic_account_id
  key_type    = var.new_relic_key_type
  ingest_type = var.new_relic_key_type
  name        = "${newrelic_cloud_aws_link_account.this.name} key"
  notes       = "AWS Cloud Integration Key for the ${var.level} account supporting ${var.app}"
}
