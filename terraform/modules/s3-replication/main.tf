resource "aws_iam_role" "main" {
  name               = local.role_name
  assume_role_policy = data.aws_iam_policy_document.source.json
}

resource "aws_iam_policy" "this" {
  name        = local.policy_name
  description = "Policy to allow s3 replication"
  policy      = data.aws_iam_policy_document.source.json
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.this.arn
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

resource "aws_s3_bucket_acl" "source_bucket_acl" {
  bucket = var.create_source_bucket ? aws_s3_bucket.source[0].id : data.aws_s3_bucket.source[0].id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "source" {
  bucket = var.create_source_bucket ? aws_s3_bucket.source[0].arn : data.aws_s3_bucket.source[0].arn
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_replication_configuration" "replication" {
  depends_on = [aws_s3_bucket_versioning.source]
  role   = aws_iam_role.main.arn
  bucket = var.create_source_bucket ? aws_s3_bucket.source[0].arn : data.aws_s3_bucket.source[0].arn
  rule {
    id = "data-loader"
    filter {
      prefix = "prod"
    }
    status = "Enabled"
    destination {
      bucket        =  "arn:aws:s3:::${var.destination_bucket_name}/*"
      storage_class = "STANDARD"
    }
  }
}


resource "aws_s3_bucket" "dest" {
  count = var.create_destination_bucket && var.enable_replication ? 1 : 0
  bucket = var.destination_bucket_name
  tags = var.tags
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_versioning" "dest" {
  count =  var.enable_replication ? 1 : 0
  bucket = var.create_destination_bucket ? aws_s3_bucket.dest[0].id : data.aws_s3_bucket.dest[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_policy" "dest" {
  count = var.enable_replication ? 1 : 0
  bucket   = var.create_destination_bucket ? aws_s3_bucket.dest[0].id : data.aws_s3_bucket.dest[0].id
  policy   = data.aws_iam_policy_document.dest[0].json
}