#create s3 bucket to store the logs
resource "aws_s3_bucket" "kinesis_log" {
  count  = var.create_kinesis ? 1:0
  bucket = local.kenesis_bucket_name
  acl    = "private"
}
resource "aws_iam_role" "firehose_role" {
  count  = var.create_kinesis ? 1:0
  name = local.kenesis_role_name
  assume_role_policy = data.aws_iam_policy_document.kinesis_assume_role_policy.json
  permissions_boundary = var.target_account_cloudone && terraform.workspace == "dev" || terraform.workspace == "qa" ? local.permission_boundary_arn: null
  tags = var.tags
}
resource "aws_iam_policy" "firehose_policy" {
  count  = var.create_kinesis ? 1:0
  name = local.kenesis_policy_name
  policy = data.aws_iam_policy_document.firehose_policy[0].json
  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "firehose_policy_attachment" {
  count  = var.create_kinesis ? 1:0
  policy_arn =  aws_iam_policy.firehose_policy[0].arn
  role       = aws_iam_role.firehose_role[0].name
}

resource "aws_kinesis_firehose_delivery_stream" "firehose_stream" {
  name        = "aws-waf-logs-${var.resource_prefix}-kinesis-firehose-stream"
  destination = "extended_s3"
  
  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.kinesis_log.arn
  }
}
