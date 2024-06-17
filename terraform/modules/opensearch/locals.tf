locals {
  access_policies       = var.create_access_policies ? data.aws_iam_policy_document.access_policy[0].json : var.access_policies
  #access_policies       = var.create_access_policies ? data.aws_iam_policy_document.access_policy.json : var.access_policies
  permissions_boundary  = var.attach_permissions_boundary ? "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PermissionBoundary_PowerUser" : null
  #security_group_ids    = var.create_security_group ? aws_security_group.this[0].id : var.security_group_ids
  security_group_ids    = var.create_security_group ? aws_security_group.this.id : var.security_group_ids
  custom_instance_type  = var.instance_type == null && var.cluster_tshirt_size != null ? lookup(local.instance_type_lookup, var.cluster_tshirt_size, null) : var.instance_type
  custom_instance_count = var.instance_count == null ? 1 : var.instance_count
  custom_volume_size    = var.volume_size == null && var.cluster_tshirt_size != null ? lookup(local.volume_size_lookup, var.cluster_tshirt_size, null) : var.volume_size


  instance_type_lookup = {
    xs = "t3.small.search"
    sm = "t3.medium.search"
    md = "m6g.large.search"
    lg = "m6g.xlarge.search"
    xl = "m6g.2xlarge.search"
  }

  volume_size_lookup = {
    xs = 10
    sm = 20
    md = 40
    lg = 80
    xl = 160
  }

  outputs = {
    security_group_arn = var.create_security_group ? aws_security_group.this[0].arn : "A Security Group was not created"
    security_group_id  = var.create_security_group ? aws_security_group.this[0].id : "A Security Group was not created"
    role_arn           = var.create_snapshot_role ? aws_iam_role.snapshot[0].arn : "A Snapshot Role was not created"
    role_id            = var.create_snapshot_role ? aws_iam_role.snapshot[0].id : "A Snapshot Role was not created"
    role_name          = var.create_snapshot_role ? aws_iam_role.snapshot[0].name : "A Snapshot Role was not created"
  }
}
