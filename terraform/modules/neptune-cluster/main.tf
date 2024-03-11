resource "aws_neptune_cluster" "this" {
  allow_major_version_upgrade          = var.allow_major_version_upgrade
  apply_immediately                    = var.apply_immediately
  backup_retention_period              = var.backup_retention_period
  cluster_identifier                   = "${var.resource_prefix}-neptune-cluster"
  copy_tags_to_snapshot                = var.copy_tags_to_snapshot
  deletion_protection                  = var.deletion_protection
  enable_cloudwatch_logs_exports       = var.enable_cloudwatch_logs_exports
  engine                               = var.engine
  engine_version                       = var.engine_version
  final_snapshot_identifier            = var.final_snapshot_identifier
  iam_roles                            = var.iam_roles
  iam_database_authentication_enabled  = var.iam_database_authentication_enabled
  kms_key_arn                          = aws_kms_key.this.arn
  neptune_subnet_group_name            = aws_neptune_subnet_group.this.name
  neptune_cluster_parameter_group_name = var.enable_serverless ? "default.neptune1.2" : module.cluster_parameters[0].name
  preferred_backup_window              = var.preferred_backup_window
  preferred_maintenance_window         = var.preferred_maintenance_window
  port                                 = var.port
  replication_source_identifier        = var.replication_source_identifier
  skip_final_snapshot                  = var.skip_final_snapshot
  snapshot_identifier                  = var.snapshot_identifier
  storage_encrypted                    = true
  vpc_security_group_ids               = var.vpc_security_group_ids

  dynamic "serverless_v2_scaling_configuration" {
    for_each = var.enable_serverless ? [1] : []

    content {
      max_capacity = var.max_capacity
      min_capacity = var.min_capacity
    }
  }
}

resource "aws_neptune_cluster_parameter_group" "this" {
  count = local.create_parameter_groups ? 1 : 0

  name        = "${var.resource_prefix}-neptune-cluster-params"
  family      = var.parameter_group_family
  description = "${var.resource_prefix} neptune cluster-level parameter group"

  parameter {
    name  = "neptune_enable_audit_log"
    value = var.enable_audit_log ? "1" : "0"
  }

  parameter {
    name  = "neptune_enable_slow_query_log"
    value = var.enable_slow_query_log
  }

  parameter {
    name  = "neptune_slow_query_log_threshold"
    value = var.slow_query_log_threshold
  }

  parameter {
    name  = "neptune_query_timeout"
    value = var.query_timeout
  }
}

resource "aws_neptune_cluster_instance" "this" {
  auto_minor_version_upgrade   = var.auto_minor_version_upgrade
  cluster_identifier           = aws_neptune_cluster.this.cluster_identifier
  engine                       = var.engine
  engine_version               = var.engine_version
  instance_class               = var.instance_class
  neptune_subnet_group_name    = aws_neptune_subnet_group.this.name
  neptune_parameter_group_name = local.create_parameter_groups ? aws_neptune_parameter_group.this[0].name : null
  port                         = var.port
  preferred_backup_window      = var.preferred_backup_window
  preferred_maintenance_window = var.preferred_maintenance_window
  publicly_accessible          = false
}

resource "aws_neptune_parameter_group" "this" {
  count = local.create_parameter_groups ? 1 : 0

  name        = "${var.resource_prefix}-neptune-instance-params"
  family      = var.parameter_group_family
  description = "${var.resource_prefix} neptune instance-level parameter group"

  parameter {
    name  = "neptune_result_cache"
    value = var.enable_result_cache ? "1" : "0"
  }
}

resource "aws_kms_key" "this" {
  deletion_window_in_days = 7
  description             = "Enforces encryption at rest for the ${terraform.workspace}-tier neptune cluster"
  key_usage               = "ENCRYPT_DECRYPT"
}

resource "aws_kms_alias" "this" {
  name          = "alias/${var.resource_prefix}-neptune-key"
  target_key_id = aws_kms_key.this.id
}

resource "aws_neptune_subnet_group" "this" {
  name        = "${var.resource_prefix}-neptune-subnets"
  description = "subnet group for the ${terraform.workspace}-tier neptune cluster"
  subnet_ids  = var.database_subnet_ids
}

resource "aws_kms_key_policy" "this" {
  key_id = aws_kms_key.this.id
  policy = data.aws_iam_policy_document.kms.json
}
