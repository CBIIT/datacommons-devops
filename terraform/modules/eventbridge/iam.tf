resource "aws_iam_role" "eventbridge_role" {
  name = "eventbridge_access_role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "events.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "eventbridge_policy" {
  role   = aws_iam_role.eventbridge_role.id

  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{
      Action   = [
        "ecs:RunTask",
        "lambda:InvokeFunction",
        "sns:Publish"
      ]
      Resource = "*"
      Effect   = "Allow"
    }]
  })
}
