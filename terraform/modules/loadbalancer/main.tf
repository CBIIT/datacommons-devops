resource "aws_lb" "alb" {
  name                       = local.alb_name
  load_balancer_type         = var.alb_type
  subnets                    = var.alb_subnet_ids
  security_groups            = [aws_security_group.alb.id]
  #tfsec:ignore:aws-elb-alb-not-public
  internal                   = var.alb_internal
  drop_invalid_header_fields = true
  enable_deletion_protection = true
  desync_mitigation_mode     = "strictest"

  access_logs {
    bucket  = var.alb_log_bucket_name
    prefix  = "alb-logs"
    enabled = true
  }

  timeouts {
    create = "15m"
  }

  tags = merge(
    {
      "Name" = format("%s-%s-lb", var.stack_name, var.env)
    },
    var.tags,
  )
}

#create https redirect
resource "aws_lb_listener" "http" {
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

  tags = var.tags
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.alb.arn
  port              = local.https_port
  protocol          = "HTTPS"
  ssl_policy        = var.alb_ssl_policy
  certificate_arn   = var.alb_certificate_arn

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = var.alb_default_message
      status_code  = "200"
    }
  }

  tags = var.tags
}

resource "aws_security_group" "alb" {
  name        = "${local.alb_name}-sg"
  description = local.alb_sg_description
  vpc_id      = var.vpc_id
  tags        = var.tags
}

resource "aws_security_group_rule" "all_egress" {
  security_group_id = aws_security_group.alb.id
  from_port         = 0
  protocol          = "-1"
  to_port           = 0
  cidr_blocks       = ["0.0.0.0/0"]
  type              = "egress"
}