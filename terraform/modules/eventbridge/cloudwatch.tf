resource "aws_cloudwatch_log_group" "eventbridge_log_group" {
  name = "/aws/events/${aws_cloudwatch_event_rule.module_event.name}"
}

resource "aws_cloudwatch_log_stream" "eventbridge_log_stream" {
  name           = "eventbridge_log_stream"
  log_group_name = aws_cloudwatch_log_group.eventbridge_log_group.name
}