# module "s3" {
#   source  = "terraform-aws-modules/s3-bucket/aws"
#   version = "3.2.3"
#   bucket = var.bucket_name
#   acl = var.bucket_acl
#   versioning = {
#     enabled = var.enable_version
#   }
#   policy = var.bucket_policy
#   lifecycle_rule = var.lifecycle_rule
#   tags = var.tags
#   attach_policy = var.attach_bucket_policy
#   force_destroy = var.force_destroy_bucket
# }

resource "aws_s3_bucket" "s3" {
  bucket        = local.bucket_name
  force_destroy = var.s3_force_destroy
  tags          = var.tags
}

resource "aws_s3_bucket_acl" "s3" {
  bucket = aws_s3_bucket.s3.id
  acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "s3" {
  bucket                  = aws_s3_bucket.s3.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
###### Need to decide if policy is passed in as variable or diff strategy?
resource "aws_s3_bucket_policy" "s3" {
  bucket = aws_s3_bucket.s3.id
  policy = var.bucket_policy #data.aws_iam_policy_document.s3.json
}

#tfsec:ignore:aws-s3-encryption-customer-key
resource "aws_s3_bucket_server_side_encryption_configuration" "s3" {
  bucket = aws_s3_bucket.s3.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "s3" {
  bucket = aws_s3_bucket.s3.id

  versioning_configuration {
    status = "Enabled"
  }

}

resource "aws_s3_bucket_lifecycle_configuration" "s3" {
  bucket = aws_s3_bucket.s3.id

  rule {
    id     = "transition_to_standard_ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }
  }

  rule {
    id     = "expire_objects"
    status = "Enabled"

    expiration {
      days = 90
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}