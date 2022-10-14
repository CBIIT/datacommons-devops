module "cloudwatch_metric_stream" {
  source = "./modules/cloudwatch-metric-stream"

  app                          = var.app
  firehose_delivery_stream_arn = module.kinesis_firehose_datastream.arn
  include_filter               = var.include_filter
  level                        = var.level
  output_format                = var.output_format
  program                      = var.program
  role_arn                     = module.iam_cloudwatch_metric_stream.role_arn

}

module "iam_cloudwatch_metric_stream" {
  source = "./modules/iam-cloudwatch-metric-stream"

  account_id              = var.account_id
  app                     = var.app
  force_detach_policies   = var.role_force_detach_policies
  iam_prefix              = var.iam_prefix
  level                   = var.level
  permission_boundary_arn = var.permission_boundary_arn
  program                 = var.program
}

module "kinesis_firehose_datastream" {
  source = "./modules/kinesis-firehose-datastream"

  app     = var.app
  level   = var.level
  program = var.program
}

module "iam_kinesis_firehose_datastream" {
  source = "./modules/iam-kinesis-firehose-datastream"

  app                     = var.app
  force_detach_policies   = var.force_detach_policies
  iam_prefix              = var.iam_prefix
  level                   = var.level
  permission_boundary_arn = var.permission_boundary_arn
  program                 = var.program

}

module "iam_read_only" {
  source = "./modules/iam-read-only"

  app                     = var.app
  force_detach_policies   = var.force_detach_policies
  iam_prefix              = var.iam_prefix
  level                   = var.level
  new_relic_account_id    = var.new_relic_account_id
  new_relic_external_id   = var.new_relic_external_id
  permission_boundary_arn = var.permission_boundary_arn
  program                 = var.program
}