locals {
  domain_name    = "${var.stack_name}-${var.env}-opensearch"
  subnets        = var.multi_az_enabled == true ? var.opensearch_subnet_ids : tolist(var.opensearch_subnet_ids[0])
  now            = timestamp()
  autotune_start = timeadd(local.now, "24h")
  #auto-tune cron format: minute hour day-of-month month day-of-week year
  #autotune expression translation: 1:00 AM on saturdays between 2022 and 2024
  autotune_reoccurance_cron = "cron(0 1 ? * 6 2022-2024)"
  sg_description            = "The security group regulating network access to the OpenSearch cluster"
  log_retention             = var.env == "dev" || var.env == "qa" ? 30 : 90
}