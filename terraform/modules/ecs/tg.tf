#create alb target group
resource "aws_lb_target_group" "target_group" {
  for_each    = var.microservices
  name        = "${var.stack_name}-${var.env}-${each.value.name}"
  port        = each.value.port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = var.alb_target_type
  stickiness {
    type            = "lb_cookie"
    cookie_duration = 1800
    enabled         = true
  }
  health_check {
    path                = each.value.health_check_path
    protocol            = "HTTP"
    matcher             = "200"
    port                = each.value.port
    interval            = 45
    timeout             = 40
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
  tags = merge(
    {
      "Name" = format("%s-%s", var.stack_name, "${each.value.name}-alb-target-group")
    },
    var.tags,
  )
}

resource "aws_lb_listener_rule" "alb_listener" {
  for_each     = var.microservices
  listener_arn = var.alb_https_listener_arn
  priority     = each.value.priority_rule_number
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group[each.key].arn
  }

  condition {
    host_header {
      values = [var.application_url]
    }
  }
  condition {
    path_pattern {
      values = each.value.path
    }
  }
}

resource "aws_lb_listener_rule" "alb_listener_additional_url" {
  count = var.stack_name == "bento" && var.env == "prod" ? 1 : 0
  listener_arn = var.alb_https_listener_arn
  action {
    type             = "forward"
    target_group_arn = data.aws_lb_target_group.frontend[count.index].arn
  }

  condition {
    host_header {
      values = [var.domain_name,"www.${var.domain_name}"]
    }
  }
}