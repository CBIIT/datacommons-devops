output "bucket_name" {
  value       = aws_s3_bucket.s3.id  #module.s3.s3_bucket_id
  description = "name of the bucket"
}

output "bucket_id" {
  value       = aws_s3_bucket.s3.id
  description = "bucket id"
}