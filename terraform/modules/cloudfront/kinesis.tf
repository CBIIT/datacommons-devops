#create s3 bucket to store the logs
resource "aws_s3_bucket" "kinesis_log" {
  bucket = local.kenesis_bucket_name
}
resource "aws_iam_role" "firehose_role" {
  name                 = local.kenesis_role_name
  assume_role_policy   = data.aws_iam_policy_document.kinesis_assume_role_policy.json
  permissions_boundary = local.permissions_boundary
  tags                 = var.tags
}
resource "aws_iam_policy" "firehose_policy" {
  name   = local.kenesis_policy_name
  policy = data.aws_iam_policy_document.firehose_policy.json
  tags   = var.tags
}

resource "aws_iam_role_policy_attachment" "firehose_policy_attachment" {
  policy_arn = aws_iam_policy.firehose_policy.arn
  role       = aws_iam_role.firehose_role.name
}

resource "aws_kinesis_firehose_delivery_stream" "firehose_stream" {
  name        = "aws-waf-logs-${var.stack_name}-${var.env}-kinesis-firehose-stream"
  destination = "s3"
  s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.kinesis_log.arn
  }
}

# resource "aws_s3_bucket_acl" "acl" {
#   bucket = aws_s3_bucket.kinesis_log.id
#   acl    = "private"
# }
#resource "aws_s3_bucket_public_access_block" "s3" {
#  bucket                  = aws_s3_bucket.kinesis_log.id
#  block_public_acls       = true
#  block_public_policy     = true
#  ignore_public_acls      = true
#  restrict_public_buckets = true
#}
