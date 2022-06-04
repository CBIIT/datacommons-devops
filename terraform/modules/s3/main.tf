module "s3" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.2.3"
  bucket = var.bucket_name
  acl = var.bucket_acl
  versioning = {
    enabled = var.enable_version
  }
  lifecycle_rule = var.lifecycle_rule
  tags = var.tags
}