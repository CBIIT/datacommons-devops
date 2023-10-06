module "cloudwatch_metric_stream" {
  source = "./modules/cloudwatch-metric-stream"

  app                          = var.app
  firehose_delivery_stream_arn = module.kinesis_firehose_datastream.arn
  include_filter               = var.include_filter
  level                        = var.level
  output_format                = var.output_format
  program                      = var.program
  role_arn                     = module.iam_cloudwatch_metric_stream.arn
  resource_prefix              = var.resource_prefix
}

module "iam_cloudwatch_metric_stream" {
  source = "./modules/iam-cloudwatch-metric-stream"

  account_id              = var.account_id
  app                     = var.app
  force_detach_policies   = var.force_detach_policies
  iam_prefix              = var.iam_prefix
  level                   = var.level
  permission_boundary_arn = var.permission_boundary_arn
  program                 = var.program
  resource_prefix         = var.resource_prefix
}

module "kinesis_firehose_datastream" {
  source = "./modules/kinesis-firehose-datastream"

  app                      = var.app
  buffer_interval          = var.buffer_interval
  buffer_size              = var.buffer_size
  content_encoding         = var.content_encoding
  destination              = var.destination
  http_endpoint_access_key = var.http_endpoint_access_key # add to vars
  http_endpoint_name       = var.http_endpoint_name
  http_endpoint_url        = var.http_endpoint_url
  level                    = var.level
  program                  = var.program
  role_arn                 = module.iam_kinesis_firehose_datastream.arn
  s3_backup_mode           = var.s3_backup_mode
  s3_bucket_arn            = var.s3_bucket_arn
  s3_compression_format    = var.s3_compression_format
  s3_error_output_prefix   = var.s3_error_output_prefix
  s3_object_prefix         = var.s3_object_prefix
  resource_prefix          = var.resource_prefix
}

module "iam_kinesis_firehose_datastream" {
  source = "./modules/iam-kinesis-firehose-datastream"

  account_id              = var.account_id
  app                     = var.app
  force_detach_policies   = var.force_detach_policies
  iam_prefix              = var.iam_prefix
  level                   = var.level
  permission_boundary_arn = var.permission_boundary_arn
  program                 = var.program
  s3_bucket_arn           = var.s3_bucket_arn
  resource_prefix         = var.resource_prefix
}

module "iam_read_only" {
  source = "./modules/iam-read-only"

  app                      = var.app
  force_detach_policies    = var.force_detach_policies
  iam_prefix               = var.iam_prefix
  level                    = var.level
  new_relic_aws_account_id = var.new_relic_aws_account_id
  new_relic_account_id     = var.new_relic_account_id
  permission_boundary_arn  = var.permission_boundary_arn
  program                  = var.program
  resource_prefix          = var.resource_prefix
}
