output "bucket_name" {
  value       = module.s3.s3_bucket_id
  description = "name of the bucket"
}