resource "aws_s3_bucket" "dest" {
  count  = var.create_destination_bucket ? 1 : 0
  bucket = var.destination_bucket_name
  tags = merge(
    {
      "CreateDate" = timestamp()
    },
    var.tags,
  )

  lifecycle {
    ignore_changes = [
      tags["CreateDate"],
    ]
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_versioning" "dest" {
  bucket = var.create_destination_bucket ? aws_s3_bucket.dest[0].id : data.aws_s3_bucket.dest[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_policy" "dest" {
  bucket = var.create_destination_bucket ? aws_s3_bucket.dest[0].id : data.aws_s3_bucket.dest[0].id
  policy = data.aws_iam_policy_document.dest.json
}