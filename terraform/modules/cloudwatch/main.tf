resource "aws_cloudwatch_event_rule" "ecs_scheduled_event" {
  name        = local.cloudwatch_event_rule_name
  description = "Scheduled event rule to run ECS task"
  schedule_expression = var.cron_expression
}

resource "aws_cloudwatch_event_target" "ecs_event_target" {
  rule      = aws_cloudwatch_event_rule.ecs_scheduled_event.name
  target_id = "run-ecs-task"

  arn = data.aws_ecs_cluster.existing_cluster.arn

  ecs_target {
    task_count          = 1
    launch_type         = var.launch_type
    platform_version    = "LATEST"
    task_definition_arn = data.aws_ecs_task_definition.existing_task.arn
  }
}

resource "aws_sns_topic" "slack_notifications" {
  name = local.sns_topic_name
}

resource "aws_sns_topic_subscription" "slack_subscription" {
  topic_arn = aws_sns_topic.slack_notifications.arn
  protocol  = "https"
  endpoint  = var.slack_notification_endpoint
}

resource "aws_iam_role" "cloudwatch_events_role" {
  name = "${var.resource_prefix}-cloudwatch-events-role"

  assume_role_policy = data.aws_iam_policy_document.cloudwatch_events_assume_role.json
}

resource "aws_iam_role_policy_attachment" "cloudwatch_events_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.cloudwatch_events_role.name
}

resource "aws_cloudwatch_event_permission" "cloudwatch_events_permission" {
  action          = "lambda:InvokeFunction"
  principal       = "events.amazonaws.com"
  source_arn      = aws_cloudwatch_event_rule.ecs_scheduled_event.arn
  statement_id    = "AllowInvoke"
  function_name   = aws_cloudwatch_event_target.ecs_event_target.arn
  source_profile  = aws_iam_role.cloudwatch_events_role.arn
}
