#task definition
resource "aws_ecs_task_definition" "task" {
  for_each                 = var.microservices
  family                   = "${var.stack_name}-${var.env}-${each.value.name}"
  network_mode             = var.ecs_network_mode
  requires_compatibilities = ["FARGATE"]
  cpu                      = each.value.cpu
  memory                   = each.value.memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = each.value.name
      image     = each.value.image_url
      essential = true
      portMappings = [
        {
          protocol      = "tcp"
          containerPort = each.value.port
          #          hostPort      = var.microservice_port
        }
      ]
    }
  ])

  tags = merge(
    {
      "Name" = format("%s-%s-%s-%s", var.stack_name, var.env, each.value.name, "task-definition")
    },
    var.tags,
  )
}

#ecs service
resource "aws_ecs_service" "service" {
  for_each                           = var.microservices
  name                               = "${var.stack_name}-${var.env}-${each.value.name}"
  cluster                            = aws_ecs_cluster.ecs_cluster.id
  task_definition                    = aws_ecs_task_definition.task[each.key].arn
  desired_count                      = each.value.number_container_replicas
  launch_type                        = var.ecs_launch_type
  scheduling_strategy                = var.ecs_scheduling_strategy
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    security_groups  = var.ecs_security_group_ids
    subnets          = var.ecs_subnet_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.target_group[each.key].arn
    container_name   = each.value.name
    container_port   = each.value.port
  }

  lifecycle {
    ignore_changes = [
      task_definition,
      desired_count
    ]
  }
}

resource "aws_appautoscaling_target" "microservice_autoscaling_target" {
  for_each           = var.microservices
  max_capacity       = 5
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.service[each.key].name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "microservice_autoscaling_cpu" {
  for_each           = var.microservices
  name               = "cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.microservice_autoscaling_target[each.key].resource_id
  scalable_dimension = aws_appautoscaling_target.microservice_autoscaling_target[each.key].scalable_dimension
  service_namespace  = aws_appautoscaling_target.microservice_autoscaling_target[each.key].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 80
  }
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.stack_name}-${var.env}-ecs"

  setting {
    name  = "containerInsights"
    value = var.container_insights_setting
  }

  configuration {
    execute_command_configuration {
      kms_key_id = aws_kms_key.ecs_exec.key_id
      logging    = var.ecs_execute_command_logging

      log_configuration {
        cloud_watch_log_group_name     = aws_cloudwatch_log_group.ecs_execute_command_log_group.name
        cloud_watch_encryption_enabled = true
      }
    }
  }

  tags = merge(
    {
      "Name" = format("%s-%s", var.stack_name, "ecs-cluster")
    },
    var.tags
  )
}
