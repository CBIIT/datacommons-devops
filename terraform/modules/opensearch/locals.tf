locals {
  domain_name    = "${var.stack_name}-${terraform.workspace}-opensearch"
  subnets        = var.multi_az_enabled ? var.opensearch_subnet_ids : [ var.opensearch_subnet_ids[0]]
  sg_description = "The security group regulating network access to the OpenSearch cluster"
  log_retention  = var.env == "dev2" || var.env == "dev" || var.env == "qa2" || var.env == "qa" ? 30 : 90
  now            = timestamp()
}