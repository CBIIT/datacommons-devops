resource "aws_efs_file_system" "efs" {
   creation_token = "efs-${var.env}"
   performance_mode = "generalPurpose"
   throughput_mode = "bursting"
   encrypted = "true"
   
   tags = merge(
    {
      "Name" = format("%s-%s-%s", var.project, var.env, "efs")
    },
    var.tags,
  )
 }

resource "aws_efs_mount_target" "efs-mt" {
   count = length(var.efs_subnet_ids)
   file_system_id  = aws_efs_file_system.efs.id
   subnet_id = var.efs_subnet_ids[count.index]
   security_groups = [aws_security_group.efs.id]
 }