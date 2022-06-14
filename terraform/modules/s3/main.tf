module "s3" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.2.3"
  bucket = var.bucket_name
  acl = var.bucket_acl
  versioning = {
    enabled = var.enable_version
  }
  policy = var.bucket_policy
  lifecycle_rule = var.lifecycle_rule
  tags = var.tags
  attach_policy = var.attach_bucket_policy
  force_destroy = var.force_destroy_bucket
}
