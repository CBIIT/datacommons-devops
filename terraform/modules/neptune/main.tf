resource "aws_neptune_cluster" "neptune_cluster" {
  apply_immediately                    = true
  backup_retention_period              = var.backup_retention_period
  cluster_identifier                   = "${var.resource_prefix}-neptune-cluster"
  deletion_protection                  = var.deletion_protection
  enable_cloudwatch_logs_exports       = ["audit"]
  engine                               = "neptune"
  engine_version                       = var.neptune_engine_version
  iam_roles                            = var.neptune_iam_roles
  neptune_subnet_group_name            = var.create_neptune_subnet_group ? aws_neptune_subnet_group.this[0].name : var.db_subnet_group_name
  port                                 = 8182
  preferred_backup_window              = var.backup_window
  preferred_maintenance_window         = var.maintenance_window #wed:04:00-wed:09:00"
  skip_final_snapshot                  = var.skip_final_snapshot
  storage_encrypted                    = var.storage_encrypted
  kms_key_arn                          = var.kms_key_arn
  vpc_security_group_ids               = var.create_neptune_security_group ? [aws_security_group.neptune[0].id] : var.vpc_security_group_ids
  tags                                 = var.tags
}

resource "aws_neptune_cluster_instance" "neptune_instance" {
  auto_minor_version_upgrade   = true
  apply_immediately            = var.apply_immediately
  neptune_subnet_group_name    = var.create_neptune_subnet_group ? aws_neptune_subnet_group.this[0].name : var.db_subnet_group_name
  preferred_maintenance_window = var.maintenance_window
  publicly_accessible          = false
  cluster_identifier           = aws_neptune_cluster.neptune_cluster.cluster_identifier
  engine                       = "neptune"
  identifier                   = "${var.resource_prefix}-neptune-instance"
  instance_class               = var.neptune_instance_class #db.serverless
  tags                         = var.tags
}

resource "aws_neptune_subnet_group" "default" {
  count = var.create_neptune_subnet_group ? 1 : 0

  name       = "${var.resource_prefix}-neptune-subnet-group"
  description = "Subnet group for ${var.resource_prefix} neptune instance"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "${var.resource_prefix}-neptune-subnet-group"
  }
}

resource "aws_security_group" "neptune" {
  count = var.create_neptune_security_group ? 1 : 0

  name  =  "${var.resource_prefix}-neptune-sg"
  vpc_id      = var.vpc_id
  description = "Allow traffic to/from neptune database"
  tags = var.tags
}

resource "aws_security_group_rule" "rds_inbound" {
  count = var.create_neptune_security_group ? 1 : 0

  description              = "From allowed SGs"
  type                     = "ingress"
  from_port                = local.neptune_port
  to_port                  = local.neptune_port
  protocol                 = local.protocol
  cidr_blocks              = var.allowed_ip_blocks
  security_group_id        = aws_security_group.neptune.id
}

resource "aws_security_group_rule" "egress" {
  count = var.create_neptune_security_group ? 1 : 0

  description       = "allow all outgoing traffic"
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = local.any
  cidr_blocks       = local.all_ips
  security_group_id =  aws_security_group.neptune.id
}
