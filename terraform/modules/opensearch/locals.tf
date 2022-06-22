locals {
  domain_name    = "${var.stack_name}-${var.env}-opensearch"
  subnets        = var.multi_az_enabled == true ? var.opensearch_subnet_ids : tolist(var.opensearch_subnet_ids[0])
  autotune_start = "2022-06-20T23:00:30.52Z"
  #auto-tune cron format: minute hour day-of-month month day-of-week year
  #autotune expression translation: 1:00 AM on saturdays between 2022 and 2024
  autotune_reoccurance_cron = "0 1 ? * 6 2022-2024"
  sg_description            = "The security group regulating network access to the OpenSearch cluster"
  log_retention             = env == "dev" || env == "qa" ? 30 : 90
}