locals {
  cloudwatch_event_rule_name = "${var.resource_prefix}-cloudwatch-event-rule"
  sns_topic_name            = "${var.resource_prefix}-sns-topic"
}
