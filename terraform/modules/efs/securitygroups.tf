resource "aws_security_group" "efs" {
   name = "${var.project}-${var.env}-efs-sg"
   description= "Allows inbound efs traffic"
   vpc_id = var.vpc_id

   tags = merge(
    {
      "Name" = format("%s-%s-%s-%s", var.project, var.env, "ecs", "sg")
    },
    var.tags
  )
}

resource "aws_security_group_rule" "all_egress" {
  security_group_id = aws_security_group.efs.id
  from_port         = 0
  protocol          = "-1"
  to_port           = 0
  cidr_blocks       = ["0.0.0.0/0"]
  type              = "egress"
}