automated_snapshot_start_hour = 23
create_os_service_role        = true
env                           = "dev"
multi_az_enabled              = true
opensearch_ebs_volume_size    = 30
opensearch_instance_count     = 2
opensearch_instance_type      = "t3.medium.elasticsearch"
opensearch_log_type           = "INDEX_SLOW_LOGS"
opensearch_logs_enabled       = true
opesearch_subnet_ids          = ["subnet-111a2222", "subnet-111b2222"]
opensearch_version            = "OpenSearch_1.2"
stack_name                    = "example"
tags = {
  ManagedBy   = "terraform"
  Program     = "program"
  Project     = "project"
  Environment = "dev"
  Region      = "us-east-1"
  POC         = "dev-lead"
}
vpc_id = "vpc-11a22222"
