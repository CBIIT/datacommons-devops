
data "aws_iam_policy_document" "s3_bucket_lb_write" {
  policy_id = "s3_bucket_lb_logs"

  statement {
    actions = [
      "s3:PutObject"
    ]
    effect    = "Allow"
    resources = ["${aws_s3_bucket.s3.arn}/*"]
    principals {
      identifiers = ["arn:aws:iam::127311923021:root"]
      type        = "AWS"
    }
  }
}


