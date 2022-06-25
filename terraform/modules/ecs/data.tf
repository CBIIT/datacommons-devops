data "aws_caller_identity" "current" {

}

data "aws_region" "current" {

}

data "aws_iam_policy_document" "ecs_exec" {
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
