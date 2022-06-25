resource "aws_kms_key" "ecs_exec" {
  description = local.kms_description
  tags = merge(
    {
      "Name" = format("%s-%s", var.stack_name, "ecs-exec-kms-key")
    },
    var.tags
  )
}
