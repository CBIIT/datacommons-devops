locals {
  domain_name = "${var.stack_name}-${var.env}-opensearch"
  subnets     = multi_az_enabled == true ? var.opensearch_subnet_ids : element(var.opensearch_subnet_ids, 0)
}