resource "aws_iam_role" "ecs_task_execution_role" {
  name               = local.task_execution_role_name
  assume_role_policy = data.aws_iam_policy_document.ecs_trust_policy
}

resource "aws_iam_role" "ecs_task_role" {
  name               = local.task_role_name
  assume_role_policy = data.aws_iam_policy_document.ecs_trust_policy
}