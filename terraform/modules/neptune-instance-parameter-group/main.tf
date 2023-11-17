resource "aws_neptune_parameter_group" "this" {
  name        = "${var.resource_prefix}-neptune-instance-params"
  family      = var.family
  description = "${var.resource_prefix} neptune instance-level parameter group"

  parameter {
    name  = "neptune_query_timeout"
    value = var.query_timeout
  }

  parameter {
    name  = "neptune_result_cache"
    value = var.enable_caching ? "1" : "0"
  }
}