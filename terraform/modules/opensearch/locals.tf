locals {
  domain_name    = "${var.stack_name}-${var.env}-opensearch"
  subnets        = var.multi_az_enabled == true ? var.opensearch_subnet_ids : tolist(var.opensearch_subnet_ids[0])
  now            = timestamp()
  autotune_start = timeadd(local.now, "24h")
  autotune_reoccurance_cron = "cron(15 1 ? * 7 2021-2024)"
  sg_description            = "The security group regulating network access to the OpenSearch cluster"
  log_retention             = var.env == "dev" || var.env == "qa" ? 30 : 90
}