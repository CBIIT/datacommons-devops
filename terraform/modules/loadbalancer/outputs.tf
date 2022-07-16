output "alb_dns_name" {
  value       = aws_lb.alb.dns_name
  description = "ALB dns name"
}

output "alb_https_listener_arn" {
  description = "https listener arn"
  value       = aws_lb_listener.https.arn
}

output "alb_zone_id" {
  description = "https listener arn"
  value       = aws_lb.alb.zone_id
}

output "alb_arn" {
  description = "the arn for the alb"
  value       = aws_lb.alb.arn
}

output "alb_securitygroup_arn" {
  description = "the arn for the security group associated with the alb"
  value       = aws_security_group.alb.arn
}

output "alb_securitygroup_id" {
  description = "the id for the security group associated with the alb"
  value       = aws_security_group.alb.id
}