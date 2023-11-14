resource "aws_neptune_cluster_instance" "this" {
  apply_immediately            = var.apply_immediately
  auto_minor_version_upgrade   = var.auto_minor_version_upgrade
  availability_zone            = var.availability_zone
  cluster_identifier           = var.cluster_identifier
  engine                       = var.engine
  engine_version               = var.engine_version
  instance_class               = var.instance_class
  neptune_subnet_group_name    = var.neptune_subnet_group_name
  neptune_parameter_group_name = var.neptune_parameter_group_name
  port                         = var.port
  promotion_tier               = var.promotion_tier
  publicly_accessible          = var.publicly_accessible
}