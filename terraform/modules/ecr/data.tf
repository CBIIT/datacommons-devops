data "aws_caller_identity" "current" {}
data "aws_region" "this" {}
data "aws_iam_policy_document" "ecr_policy_doc" {

  statement {
    sid    = "ElasticContainerRegistryPushAndPull"
    effect = "Allow"

    principals {
      identifiers = [local.account_arn]
      type        = "AWS"
    }
    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
    ]
  }
}
data "aws_iam_policy_document" "replication" {
  count = var.enable_ecr_replication ? 1 : 0
  statement {
    effect = "Allow"
    principals {
      identifiers = ["arn:aws:iam::${var.replication_destination_registry_id}:root"]
      type        = "AWS"
    }
    actions = [
      "ecr:CreateRepository",
      "ecr:ReplicateImage"
    ]
    resources = [
      "arn:aws:ecr:${data.aws_region.this.name}:${data.aws_caller_identity.current.account_id}:repository/*"
    ]
  }
}