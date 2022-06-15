locals {
  http_port          = 80
  https_port         = "443"
  alb_name           = "${var.stack_name}-${var.env}-alb"
  alb_sg_description = "The security group attached to the ${var.app}-alb-${var.tier} application load balancer"
}