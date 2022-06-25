data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

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

# combine all policy docs defined below (keeping things modular)
data "aws_iam_policy_document" "ecs_task_role_exec_policy_doc" {
  source_policy_documents = [
    data.aws_iam_policy_document.ecs_exec_command.json,
    data.aws_iam_policy_document.ecs_exec_ssm.json,
    data.aws_iam_policy_document.ecs_exec_cloudwatch.json,
    data.aws_iam_policy_document.ecs_exec_kms.json
  ]
}

data "aws_iam_policy_document" "ecs_exec_command" {
  statement {
    effect    = "Allow"
    actions   = ["ecs:ExecuteCommand"]
    resources = [aws_ecs_cluster.ecs_cluster.arn]

    condition {
      test     = "StringEquals"
      values   = [var.stack_name]
      variable = "aws:ResourceTag/tag-value"
    }
  }
}

data "aws_iam_policy_document" "ecs_exec_ssm" {

  #refine for all SSM in account
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
      "logs:DescribeLogGroups"
    ]
    resources = [
      "arn:aws:logs:${aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*",
      "arn:aws:logs:${aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*:*"]
  }

  #need to refine this to exec log groups be referencing ARN in resources
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents"
    ]
    resources = ["${aws_cloudwatch_log_group.arn}/*"]
  }
}

data "aws_iam_policy_document" "ecs_exec_kms" {
  #refine for KMS key
  statement {
    effect    = "Allow"
    actions   = [
      "kms:Decrypt",
      "kms:GenerateDataKey"
      ]
    resources = [aws_kms_key.ecs_exec.arn]
  }
}

