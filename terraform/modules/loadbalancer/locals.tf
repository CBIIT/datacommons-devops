locals {
  http_port          = 80
  https_port         = "443"
  alb_name           = "${var.resource_prefix}-alb"
  alb_sg_description = "The security group attached to the ${var.resource_prefix}-alb application load balancer"
}