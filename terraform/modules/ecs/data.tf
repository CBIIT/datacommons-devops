data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_vpc" "current" {
  id = var.vpc_id
}

data "aws_iam_policy_document" "ecs_trust_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}


# combine several below policies to define the task_execution_role (keeping things modular)
data "aws_iam_policy_document" "ecs_task_execution_role_policy_doc" {
  source_policy_documents = [
    data.aws_iam_policy_document.task_execution_ecr.json,
    data.aws_iam_policy_document.task_execution_secrets.json,
    data.aws_iam_policy_document.task_execution_kms.json,
    data.aws_iam_policy_document.ecs_exec_cloudwatch.json,
  ]
}

data "aws_iam_policy_document" "task_execution_kms" {
  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey"
    ]
    resources = ["arn:aws:kms:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:key/*"]
  }
}

data "aws_iam_policy_document" "task_execution_secrets" {
  statement {
  effect = "Allow"
  actions = [
    "secretsmanager:GetSecretValue",
    "secretsmanager:ListSecrets",
    "secretsmanager:DescribeSecret",
    "secretsmanager:ListSecretVersionIds",
    "secretsmanager:GetResourcePolicy"
  ]
  resources = ["arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:*"]
  }
}

data "aws_iam_policy_document" "task_execution_ecr" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:BatchGetImage",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "ecr:CompleteLayerUpload",
      "ecr:DescribeRepositories",
      "ecr:GetLifecyclePolicy",
      "ecr:GetRepositoryPolicy",
      "ecr:InitiateLayerUpload",
      "ecr:ListTagsForResource",
      "ecr:UploadLayerPart",
    ]
    resources = ["arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken"
    ]
    resources = ["*"]
  }
}

# combine all policy docs defined below for the task_role (keeping things modular)

data "aws_iam_policy_document" "ecs_task_role_exec_policy_doc" {
  source_policy_documents = [
    data.aws_iam_policy_document.ecs_exec_command.json,
    data.aws_iam_policy_document.task_execution_ecr.json,
    data.aws_iam_policy_document.ecs_exec_ssm.json,
    data.aws_iam_policy_document.ecs_exec_cloudwatch.json,
    data.aws_iam_policy_document.ecs_exec_kms.json,
    data.aws_iam_policy_document.task_execution_secrets.json,
    data.aws_iam_policy_document.os_policy.json
  ]
}

data "aws_iam_policy_document" "ecs_exec_command" {
  statement {
    effect    = "Allow"
    actions   = ["ecs:ExecuteCommand"]
    resources = [aws_ecs_cluster.ecs_cluster.arn]
  }
}

data "aws_iam_policy_document" "ecs_exec_ssm" {

  #this can't be refined, no resource types for ssm
  statement {
    effect = "Allow"
    actions = [
      "ssmmessages:CreateControlChannel",
      "ssmmessages:CreateDataChannel",
      "ssmmessages:OpenControlChannel",
      "ssmmessages:OpenDataChannel"
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "ecs_exec_cloudwatch" {

  #need to refine this to all log groups in the account
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStreams",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:CreateLogGroup"
    ]
    resources = [aws_cloudwatch_log_group.ecs_execute_command_log_group.arn]
  }

  #need to refine this to exec log groups be referencing ARN in resources
  statement {
    effect = "Allow"
    actions = [
      "logs:PutLogEvents"
    ]
    resources = [
      "${aws_cloudwatch_log_group.ecs_execute_command_log_group.arn}:*"
    ]
  }
}

data "aws_iam_policy_document" "ecs_exec_kms" {

  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
      "kms:GenerateDataKey"
    ]
    resources = [aws_kms_key.ecs_exec.arn]
  }
}

data "aws_iam_policy_document" "os_policy" {
  statement {
    effect = "Allow"
    actions = ["es:ESHttp*"]
    resources = ["arn:aws:es:*:${data.aws_caller_identity.current.account_id}:domain/${local.os_domain_name}/*"]
  }
}

