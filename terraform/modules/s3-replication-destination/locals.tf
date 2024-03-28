locals {
  destination_bucket_arn = var.create_destination_bucket ? aws_s3_bucket.dest[0].arn : data.aws_s3_bucket.dest[0].arn
}