resource "aws_s3_bucket" "s3" {
	# checkov:skip=CKV_AWS_145: Ignore customer managed key (cmk) warning
	# checkov:skip=CKV_AWS_144: Ignore cross-region replication warnings
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
    status = var.s3_versioning_status
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_lifecycle" {
  rule {
    id      = "tmp-files-rule"
    status = "Enabled"

    filter {
      prefix = "tmp/"
    }

    expiration {
      days = 2
    }
  }

  bucket = aws_s3_bucket.s3.id
}

resource "aws_s3_bucket_intelligent_tiering_configuration" "s3" {
  bucket = aws_s3_bucket.s3.bucket
  name = "${local.bucket_name}-intelligent-tiering"

  status = var.s3_intelligent_tiering_status

  tiering {
    access_tier = "ARCHIVE_ACCESS"
    days = var.days_for_archive_tiering
  }

  tiering {
    access_tier = "DEEP_ARCHIVE_ACCESS"
    days = var.days_for_deep_archive_tiering
  }
}

resource "aws_s3_bucket_logging" "s3" {
  count = var.s3_enable_access_logging == true ? 1 : 0
  
  bucket = aws_s3_bucket.s3.id
  target_bucket = var.s3_access_log_bucket_id
  target_prefix = var.s3_log_prefix
}
