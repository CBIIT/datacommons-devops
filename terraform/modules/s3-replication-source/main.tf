resource "aws_iam_role" "main" {
  name                 = local.role_name
  assume_role_policy   = data.aws_iam_policy_document.main.json
  permissions_boundary =  local.permission_boundary_arn
}

resource "aws_iam_policy" "main" {
  name        = local.policy_name
  description = "Policy to allow s3 replication"
  policy      = data.aws_iam_policy_document.source.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_s3_bucket" "source" {
  count = var.create_source_bucket ? 1 : 0
  bucket   =  var.source_bucket_name
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_versioning" "source" {
  bucket = var.create_source_bucket ? aws_s3_bucket.source[0].id : data.aws_s3_bucket.source[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_replication_configuration" "replication" {
  depends_on = [aws_s3_bucket_versioning.source]
  role   = aws_iam_role.main.arn
  bucket = var.create_source_bucket ? aws_s3_bucket.source[0].id : data.aws_s3_bucket.source[0].id
  rule {
    id = "data-loader"
    filter {
      prefix = "prod"
    }
    delete_marker_replication {
      status = "Enabled"
    }
    status = "Enabled"
    destination {
      bucket        =  "arn:aws:s3:::${var.destination_bucket_name}"
      storage_class = "STANDARD"
    }
  }
}
