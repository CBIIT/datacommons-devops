resource "aws_ecr_repository" "ecr" {
  for_each             = toset(var.ecr_repo_names)
  name                 = "${local.ecr_repo_prefix}-${each.key}"
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

resource "aws_ecr_registry_policy" "this" {
  count = var.enable_ecr_replication ? 1: 0
  policy = data.aws_iam_policy_document.replication[0].json
}

resource "aws_ecr_replication_configuration" "replication" {
  count = var.enable_ecr_replication ? 1: 0
  replication_configuration {
    rule {
      destination {
        region      = data.aws_region.this.name
        registry_id = var.replication_destination_registry_id
      }
    }
  }
}