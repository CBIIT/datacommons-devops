public_subnet_ids = [
  "subnet-03bb1c845d35aacc5",
  "subnet-0a575f7e0c97cad77"
]
private_subnet_ids = [
  "subnet-09b0c7407416d4730",
  "subnet-07d177a4d9df5cd32"
]
vpc_id = "vpc-08f154f94dc8a0e34"
stack_name = "mtu"
app_name = "mtu"
profile = "icdc"
domain_name = "bento-tools.org"

tags = {
  Project = "mtu"
  CreatedWith = "Terraform"
  POC = "ye.wu@nih.gov"
  Environment = "dev"
}
certificate_domain_name = "*.bento-tools.org"
allowed_subnet_ip_block = ["172.18.0.0/16"]
app_sub_domain = "mtu-dev"
elasticsearch_version = "1.1"
region = "us-east-1"
elasticsearch_instance_type = "t3.medium.elasticsearch"
create_es_service_role = false

microservices  = {
  frontend = {
    name = "frontend"
    port = 80
    health_check_path = "/"
    priority_rule_number = 20
    image_url = "cbiitssrepo/bento-frontend:latest"
    cpu = 256
    memory = 512
    path = "/*"
  },
  backend = {
    name = "backend"
    port = 8080
    health_check_path = "/ping"
    priority_rule_number = 20
    image_url = "cbiitssrepo/bento-frontend:latest"
    cpu = 512
    memory = 1024
    path = "/v1/graphql/*"
  },
  frontend = {
    name = "auth"
    port = 8082
    health_check_path = "/api/auth/ping"
    priority_rule_number = 20
    image_url = "cbiitssrepo/bento-auth:latest"
    cpu = 256
    memory = 512
    path = "/api/auth/*"
  }

}