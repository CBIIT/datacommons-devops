resource "aws_ecr_repository" "ecr" {
  for_each             = toset(var.ecr_repo_names)
  name                 = "${var.resource_prefix}-${each.key}"
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
  policy     = local.policy_doc
}

resource "aws_ecr_lifecycle_policy" "ecr_life_cycle" {
  for_each   = toset(var.ecr_repo_names)
  repository = aws_ecr_repository.ecr[each.key].name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "keep last ${var.max_images_to_keep} images"
      action = {
        type = "expire"
      }
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = var.max_images_to_keep
      }
    }]
  })
}

resource "aws_ecr_registry_policy" "this" {
  count = var.allow_ecr_replication ? 1: 0
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "Replication",
        Effect = "Allow",
        Principal = {
          "AWS" : "arn:aws:iam::${var.replication_source_registry_id}:root"
        },
        Action = [
          "ecr:CreateRepository",
          "ecr:ReplicateImage"
        ],
        Resource = [
          "arn:aws:ecr:${data.aws_region.this.name}:${data.aws_caller_identity.current.account_id}:repository/*"
        ]
      }
    ]
  })
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