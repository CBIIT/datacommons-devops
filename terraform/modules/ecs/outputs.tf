# ECS Outputs:
output "ecs_task_definition_arn" {
  value = {for k, v in aws_ecs_task_definition.task: k => v.arn}
}

output "ecs_task_service_arn" {
  value = {for k, v in aws_ecs_service.service: k => v.id}
}
/* output "appautoscaling_target_arn" {
  value = {for k, v in aws_appautoscaling_target.microservice_autoscaling_target: k => v.arn}
} */

output "appautoscaling_policy_arn" {
  value = {for k, v in aws_appautoscaling_policy.microservice_autoscaling_cpu: k => v.arn}
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.ecs_cluster.arn
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.ecs_cluster.name
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

# security group outputs

output "ecs_security_group_id" {
  value = aws_security_group.ecs.id
}

output "ecs_security_group_arn" {
  value = aws_security_group.ecs.arn
}

output "app_security_group_id" {
  value = aws_security_group.app.id
}

output "app_security_group_arn" {
  value = aws_security_group.app.arn
}
