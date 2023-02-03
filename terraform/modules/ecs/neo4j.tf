#task definition
resource "aws_ecs_task_definition" "neo4j" {
  count = var.create_neo4j_db ? 1 : 0
  family                   = "${var.stack_name}-${var.env}-neo4j-db"
  network_mode             = var.ecs_network_mode
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "neo4j"
      image     = "neo4j:5.3.0"
      essential = true
      portMappings = [
        {
          protocol      = "tcp"
          containerPort = 7474
        },
        {
          protocol      = "tcp"
          containerPort = 7687
        }
      ]
    }
  ])

  tags = merge(
  {
    "Name" = format("%s-%s-%s-%s", var.stack_name, var.env, "neo4j", "task-definition")
  },
  var.tags,
  )
}

#ecs service
resource "aws_ecs_service" "neo4j" {
  count = var.create_neo4j_db ? 1 : 0
  name                               = "${var.stack_name}-${var.env}-neo4j"
  cluster                            = aws_ecs_cluster.ecs_cluster.id
  task_definition                    = aws_ecs_task_definition.neo4j[0].arn
  desired_count                      = 1
  launch_type                        = var.ecs_launch_type
  scheduling_strategy                = var.ecs_scheduling_strategy
  deployment_minimum_healthy_percent = 50
  deployment_maximum_percent         = 200

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    security_groups  = [ aws_security_group.ecs.id,aws_security_group.app.id]
    subnets          = var.ecs_subnet_ids
    assign_public_ip = false
  }

  lifecycle {
    ignore_changes = [
      task_definition,
      desired_count
    ]
  }
}

resource "aws_appautoscaling_target" "neo4j_autoscaling_target" {
  count = var.create_neo4j_db ? 1 : 0
  max_capacity       = 5
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.neo4j[0].name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "neo4j_autoscaling_cpu" {
  count = var.create_neo4j_db ? 1 : 0
  name               = "cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.neo4j_autoscaling_target[0].resource_id
  scalable_dimension = aws_appautoscaling_target.neo4j_autoscaling_target[0].scalable_dimension
  service_namespace  = aws_appautoscaling_target.neo4j_autoscaling_target[0].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 80
  }
}
