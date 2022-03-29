#task definition
resource "aws_ecs_task_definition" "task" {
  family        = "${var.stack_name}-${var.env}-${var.microservice_name}"
  network_mode  = var.ecs_network_mode
  requires_compatibilities = ["FARGATE"]
  cpu = var.microservice_cpu
  memory = var.microservice_memory
  execution_role_arn =  aws_iam_role.task_execution_role.arn
  task_role_arn = aws_iam_role.task_role.arn
  container_definitions = jsonencode([
    {
      name         =  var.microservice_name
      image        =  var.microservice_container_image_name
      essential    = true
      portMappings = [
        {
          protocol      = "tcp"
          containerPort = var.microservice_port
          hostPort      = var.microservice_port
        }
      ]
    }])
  tags = merge(
  {
    "Name" = format("%s-%s-%s",var.stack_name,var.env,"task-definition")
  },
  var.tags,
  )
}
#ecs service
resource "aws_ecs_service" "service" {
  name              = "${var.stack_name}-${var.env}-${var.microservice_name}"
  cluster           = aws_ecs_cluster.ecs_cluster.id
  task_definition   = aws_ecs_task_definition.task.arn
  desired_count     = var.number_container_replicas
  launch_type       = var.ecs_launch_type
  scheduling_strategy = var.ecs_scheduling_strategy
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200
  network_configuration {
    security_groups  = [aws_security_group.app_sg.id]
    subnets          = var.private_subnet_ids
    assign_public_ip = false
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name   =  var.microservice_name
    container_port   = var.microservice_port
  }
  lifecycle {
    ignore_changes = [task_definition, desired_count]
  }
}


#create ecs cluster
resource "aws_appautoscaling_target" "microservice_autoscaling_target" {
  max_capacity       = 5
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "microservice_autoscaling_cpu" {
  name               = "cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.microservice_autoscaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.microservice_autoscaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.microservice_autoscaling_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value       = 80
  }
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.stack_name}-${var.env}-ecs"
  tags = merge(
  {
    "Name" = format("%s-%s",var.stack_name,"ecs-cluster")
  },
  var.tags,
  )

}

resource "aws_security_group" "app_sg" {
  name = "${var.stack_name}-${var.env}-app-sg"
  vpc_id = var.vpc_id
  tags = merge(
  {
    "Name" = format("%s-%s-frontend-sg",var.stack_name,var.env),
  },
  var.tags,
  )
}

resource "aws_security_group_rule" "inbound_alb" {
  from_port = var.microservice_port
  protocol = local.tcp_protocol
  to_port = var.microservice_port
  security_group_id = aws_security_group.app_sg.id
  source_security_group_id = aws_security_group.alb-sg.id
  type = "ingress"
}



resource "aws_security_group_rule" "all_outbound_frontend" {
  from_port = local.any_port
  protocol = local.any_protocol
  to_port = local.any_port
  cidr_blocks = local.all_ips
  security_group_id = aws_security_group.app_sg.id
  type = "egress"
}

#create alb target group
resource "aws_lb_target_group" "target_group" {
  name = "${var.stack_name}-${var.env}-${var.microservice_name}"
  port = var.microservice_port
  protocol = "HTTP"
  vpc_id =  var.vpc_id
  target_type = var.alb_target_type
  stickiness {
    type = "lb_cookie"
    cookie_duration = 1800
    enabled = true
  }
  health_check {
    path = var.microservice_path
    protocol = "HTTP"
    matcher = "200"
    interval = 15
    timeout = 3
    healthy_threshold = 2
    unhealthy_threshold = 2
  }
  tags = merge(
  {
    "Name" = format("%s-%s",var.stack_name,"${var.microservice_name}-alb-target-group")
  },
  var.tags,
  )
}

resource "aws_lb_listener_rule" "alb_listener" {
  listener_arn = aws_lb_listener.listener_https.arn
  priority = var.microservice_priority_rule_number
  action {
    type = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }

  condition {
    host_header {
      values = [var.microservice_url]
    }
  }
  condition {
    path_pattern  {
      values = [var.microservice_path]
    }
  }
}

