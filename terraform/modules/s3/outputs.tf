output "bucket_name" {
  value       = aws_s3_bucket.s3.s3_bucket_id  #module.s3.s3_bucket_id
  description = "name of the bucket"
}