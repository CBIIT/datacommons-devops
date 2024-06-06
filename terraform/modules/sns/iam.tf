resource "aws_iam_role" "sns_publish_role" {
  name = "${var.resource_prefix}-${var.sns_topic_name}-publish-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "sns.amazonaws.com",
        },
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "sns_publish_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.sns_publish_role.name
}

resource "aws_sns_topic_policy" "sns_publish_policy" {
  name = "${var.resource_prefix}-${var.sns_topic_name}-publish-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "sns:Publish",
        Resource = aws_sns_topic.main.arn,
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

