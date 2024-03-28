resource "aws_kms_key" "ecs_exec" {
  description         = local.kms_description
  enable_key_rotation = true

  tags = merge(
    {
      "Name"       = format("%s-%s", var.stack_name, "ecs-exec-kms-key"),
      "CreateDate" = timestamp()
    },
    var.tags,
  )

  lifecycle {
    ignore_changes = [
      tags["CreateDate"],
    ]
  }

}
