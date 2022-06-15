locals {
  account_arn = format("arn:aws:iam::%s:root", data.aws_caller_identity.current.account_id)
}
data "aws_caller_identity" "current" {}
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
resource "aws_ecr_repository" "ecr" {
  for_each             = toset(var.ecr_repo_names)
  name                 = "${var.stack_name}-${each.key}"
  image_tag_mutability = "MUTABLE"
  tags = merge(
    {
      "Name" = format("%s-%s-%s", each.key, var.env, "ecr-registry")
    },
    var.tags,
  )
}

resource "aws_ecr_repository_policy" "ecr_policy" {
  for_each   = toset(var.ecr_repo_names)
  repository = aws_ecr_repository.ecr[each.key].name
  policy     = data.aws_iam_policy_document.ecr_policy_doc.json
}

resource "aws_ecr_lifecycle_policy" "ecr_life_cycle" {
  for_each   = toset(var.ecr_repo_names)
  repository = aws_ecr_repository.ecr[each.key].name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "keep last 20 images"
      action = {
        type = "expire"
      }
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 15
      }
    }]
  })
}