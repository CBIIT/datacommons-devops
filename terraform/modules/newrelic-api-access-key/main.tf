resource "newrelic_api_access_key" "this" {
  account_id  = var.new_relic_account_id
  key_type    = var.new_relic_key_type
  ingest_type = var.new_relic_ingest_type
  name        = "${var.program}-${var.level}-${var.app}"
  notes       = "AWS Cloud Integration Key for the ${var.level} account supporting ${var.app}"
}
