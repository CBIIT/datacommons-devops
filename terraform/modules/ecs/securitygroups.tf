resource "aws_security_group" "ecs" {
  name        = "${var.stack_name}-${var.env}-ecs-sg"
  description = "The security group controlling access to Fargate/ECS resources"
  vpc_id      = var.vpc_id

  tags = merge(
    {
      "Name" = format("%s-%s-%s-%s", var.stack_name, var.env, "ecs", "sg")
    },
    var.tags
  )
}


resource "aws_security_group_rule" "all_egress" {
  security_group_id = aws_security_group.ecs.id
  from_port         = 0
  protocol          = "-1"
  to_port           = 0
  cidr_blocks       = ["0.0.0.0/0"]
  type              = "egress"
}

#create app security group
resource "aws_security_group" "app" {
  name = "${var.stack_name}-${var.env}-app-sg"
  description       = "Allow application to communicate with other aws resources"
  vpc_id = var.vpc_id
  tags = merge(
  {
    "Name" = format("%s-%s-app-sg",var.stack_name,terraform.workspace),
  },
  var.tags,
  )
}

resource "aws_security_group_rule" "app_all_egress" {
  security_group_id = aws_security_group.app.id
  from_port         = 0
  protocol          = "-1"
  to_port           = 0
  cidr_blocks       = ["0.0.0.0/0"]
  type              = "egress"
}