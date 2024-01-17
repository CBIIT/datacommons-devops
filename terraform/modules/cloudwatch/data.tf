data "aws_iam_policy_document" "cloudwatch_events_assume_role" {
    statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "cloudwatch_events_target" {
    statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

data "aws_ecs_cluster" "existing_cluster" {
  name = var.ecs_cluster_name
}

data "aws_ecs_task_definition" "existing_task" {
  task_definition = var.ecs_task_definition
}