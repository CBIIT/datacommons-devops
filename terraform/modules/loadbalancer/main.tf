locals {
  http_port    = 80
  any_port     = 0
  any_protocol = "-1"
  tcp_protocol = "tcp"
  https_port   = "443"
}
data "aws_acm_certificate" "cert" {
  domain      = var.certificate_domain_name
  types       = [var.acm_certificate_issued_type]
  most_recent = true
}

resource "aws_lb" "alb" {
  name               = "${var.stack_name}-${var.alb_name}-${var.env}"
  load_balancer_type = var.lb_type
  subnets            = var.alb_subnet_ids
  security_groups    = var.alb_security_group_ids
  internal = var.internal_alb
  access_logs  {
    bucket  = var.alb_log_bucket_name
    prefix  = "alb-logs"
    enabled = true
  }

  timeouts {
    create = "15m"
  }

  tags = merge(
  {
    "Name" = format("%s-%s-alb", var.stack_name, var.env)
  },
  var.tags,
  )
}

#create https redirect
resource "aws_lb_listener" "redirect_https" {
  load_balancer_arn = aws_lb.alb.arn
  port              = local.http_port
  protocol          = "HTTP"
  default_action {
    type = "redirect"
    redirect {
      port        = local.https_port
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "listener_https" {
  load_balancer_arn = aws_lb.alb.arn
  port              = local.https_port
  protocol          = "HTTPS"
  ssl_policy        = var.ssl_policy
  certificate_arn   = data.aws_acm_certificate.cert.arn
  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = var.default_message
      status_code  = "200"
    }
  }
}
