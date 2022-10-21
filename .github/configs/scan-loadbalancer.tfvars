alb_certificate     = "abc-xyz"
alb_default_message = "default message"
alb_internal        = true
alb_log_bucket_name = "example-alb-log-bucket-name"
alb_ssl_policy      = "ELBSecurityPolicy-TLS-1-2-Ext-2018-06"
alb_subnet_ids      = ["subnet-111a2222", "subnet-111b2222"]
alb_type            = "internal"
env                 = "demo"
stack_name          = "example"
tags = {
  ManagedBy   = "terraform"
  Program     = "program"
  Project     = "project"
  Environment = "dev"
  Region      = "us-east-1"
  POC         = "dev-lead"
}
vpc_id = "vpc-11a22222"
