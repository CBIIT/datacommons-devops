module "opensearch" {
  source = "../.."


  attach_permissions_boundary = true
  cluster_tshirt_size         = "md"
  engine_version              = "OpenSearch_2.11"
  resource_prefix             = "program-tier-app"
  s3_snapshot_bucket_arn      = "arn:aws:s3:::basic-example-snapshot-bucket"
  subnet_ids                  = ["subnet-01234567891011121", "subnet-abcdefghijklmnopq"]
  vpc_id                      = "vpc-01234567891011121"
}
