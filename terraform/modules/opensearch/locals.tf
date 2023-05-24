locals {
  domain_name    = "${var.resource_prefix}-opensearch"
  subnets        = var.multi_az_enabled ? var.opensearch_subnet_ids : [ var.opensearch_subnet_ids[0]]
  sg_description = "The security group regulating network access to the OpenSearch cluster"
  log_retention  = var.env == "dev" || var.env == "qa" ? 30 : 90
  now            = timestamp()
}