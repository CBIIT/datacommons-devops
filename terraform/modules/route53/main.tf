resource "aws_route53_record" "dns_record" {
  name = "${var.application_subdomain}-${var.env}"
  type = "A"
  zone_id = data.aws_route53_zone.zone.id
  alias {
    evaluate_target_health = false
    name = var.alb_dns_name
    zone_id = var.alb_zone_id
  }
}
