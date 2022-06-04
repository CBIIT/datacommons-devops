locals {
  all_ips      = ["0.0.0.0/0"]
  alb_subnets = terraform.workspace == "prod" || terraform.workspace == "stage" ? var.public_subnet_ids : var.private_subnet_ids
  app_url =  terraform.workspace == "prod" ? "${var.app_sub_domain}.${var.domain_name}" : "${var.app_sub_domain}-${terraform.workspace}.${var.domain_name}"
  nih_ip_cidrs = [ "129.43.0.0/16" , "137.187.0.0/16" , "10.128.0.0/9" , "165.112.0.0/16" , "156.40.0.0/16" , "10.208.0.0/21" , "128.231.0.0/16" , "130.14.0.0/16" , "157.98.0.0/16" , "10.133.0.0/16" ]
  alb_allowed_ip_range = terraform.workspace == "prod" || terraform.workspace == "stage" ?  local.all_ips : local.nih_ip_cidrs
}

#create ecs cluster
module "ecs" {
  for_each = var.microservices
  source = "../modules/ecs"
  alb_allowed_ip_range = local.alb_allowed_ip_range
  alb_subnets = local.alb_subnets
  certificate_domain_name = var.certificate_domain_name
  domain_name = var.domain_name
  stack_name = var.stack_name
  tags =  var.tags
  vpc_id = var.vpc_id
  env = terraform.workspace
  microservice_container_image_name = each.value["image"]
  microservice_cpu = each.value["cpu"]
  microservice_health_check_path = each.value["health_check_path"]
  microservice_memory = each.value["memory"]
  microservice_name = each.value["name"]
  microservice_path = each.value["path"]
  microservice_priority_rule_number = each.value["priority_rule_number"]
  microservice_url = local.app_url
}

#create opensearch
module "opensearch" {
  source = "../modules/opensearch"
  stack_name = var.stack_name
  tags = var.tags
  vpc_id = var.vpc_id
  elasticsearch_instance_type = var.elasticsearch_instance_type
  env = terraform.workspace
  private_subnet_ids = var.private_subnet_ids
  elasticsearch_version = var.elasticsearch_version
  allowed_subnet_ip_block = var.allowed_subnet_ip_block
}