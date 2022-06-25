data "aws_caller_identity" "current" {

}

data "aws_region" "current" {

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
     resources = [ "*" ]
  }
}

data "aws_iam_policy_document" "ecs_exec_cloudwatch" {
  
  #need to refine this to all log groups in the account
  statement {
    effect = "Allow"
    actions = [ 
      "logs:DescribeLogGroups"
     ]
    resources = [ "*" ]
  }

  #need to refine this to exec log groups be referencing ARN in resources
  statement {
    effect = "Allow"
    actions = [ 
      "logs:CreateLogStream",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents"
     ]
    resources = [ "*" ]
  }
}

data "aws_iam_policy_document" "ecs_exec_s3" {

  #need to conditionally create an S3 bucket for the logs? creating s3 should be something done outside of module?
  statement {
    effect = "Allow"
    actions = [ "s3:PutObject" ]
    resources = [ "${var.ecs_exec_log_bucket}/*" ]
  }

  #need to conditionally create an S3 bucket for the logs? creating s3 should be something done outside of module?
  statement {
    effect = "Allow"
    actions = [ "s3:GetEncryptionConfiguration" ]
    resources = var.ecs_exec_log_bucket
  }

  #refine for KMS key
  statement {
    effect = "Allow"
    actions = [ "kms:Decrypt" ]
    resources = [ "*" ]
  }
}
