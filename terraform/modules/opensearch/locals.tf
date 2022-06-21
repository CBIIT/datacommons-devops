locals {
  domain_name = "${var.stack_name}-${var.env}-opensearch"
  subnets     = multi_az_enabled == true ? var.opensearch_subnet_ids : element(var.opensearch_subnet_ids, 0)
  autotune_start = "2022-06-20T23:00:30-0400"
  autotune_reoccurance_cron = "0 59 23 ? 0 0"
}