resource "aws_iam_role" "ecs_task_execution_role" {
  name                 = local.task_execution_role_name
  assume_role_policy   = data.aws_iam_policy_document.ecs_trust_policy.json
  permissions_boundary = local.permission_boundary_arn
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_execution_role_policy.arn
}

resource "aws_iam_policy" "ecs_task_execution_role_policy" {
  name   = local.task_execution_role_policy_name
  policy = data.aws_iam_policy_document.ecs_task_execution_role_policy_doc.json
}

resource "aws_iam_role" "ecs_task_role" {
  name                 = local.task_role_name
  assume_role_policy   = data.aws_iam_policy_document.ecs_trust_policy.json
  permissions_boundary = local.permission_boundary_arn
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_exec_attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_task_role_exec_policy.arn
}

resource "aws_iam_policy" "ecs_task_role_exec_policy" {
  name   = local.task_role_policy_exec_name
  policy = data.aws_iam_policy_document.ecs_task_role_exec_policy_doc.json
} 