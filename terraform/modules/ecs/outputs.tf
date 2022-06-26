# ECS Outputs:
output "ecs_task_definition_arn" {
  value = aws_ecs_task_definition.task.arn
}

output "ecs_task_service_arn" {
  value = aws_ecs_service.service.arn
}

output "appautoscaling_target_arn" {
  value = aws_appautoscaling_target.microservice_autoscaling_target.arn
}

output "appautoscaling_policy_arn" {
  value = aws_appautoscaling_policy.microservice_autoscaling_cpu.arn
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.ecs_cluster.arn
}

# IAM Outputs: 
output "ecs_task_execution_role_name" {
  value = aws_iam_role.ecs_task_execution_role.name
}

output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "ecs_task_role_name" {
  value = aws_iam_role.ecs_task_role.name
}

output "ecs_task_role_arn" {
  value = aws_iam_role.ecs_task_role.arn
}

output "ecs_security_group_id" {
  value = aws_security_group.ecs.id
}

output "ecs_security_group_arn" {
  value = aws_security_group.ecs.arn
}