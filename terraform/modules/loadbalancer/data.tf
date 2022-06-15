data "aws_acm_certificate" "cert" {
  domain      = var.certificate_domain_name
  types       = [var.acm_certificate_issued_type]
  most_recent = true
}