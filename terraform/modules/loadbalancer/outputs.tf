output "alb_dns_name" {
  value = aws_lb.alb.dns_name
  description = "ALB dns name"
}
output "alb_https_listener_arn" {
  description = "https listener arn"
  value = aws_lb_listener.listener_https.arn
}
output "alb_zone_id" {
  description = "https listener arn"
  value = aws_lb.alb.zone_id
}