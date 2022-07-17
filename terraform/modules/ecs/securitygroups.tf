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

resource "aws_security_group_rule" "nih_network_ingress" {
  count = var.target_account_cloudone ? 1: 0
  security_group_id = aws_security_group.ecs.id
  description       = "Allow ingress network access to the ECS security group specified by CIDR Blocks"
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 80
  to_port           = 80
  cidr_blocks       = local.nih_cidr_ranges

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
  count = var.create_app_security_group ? 1 : 0
  name = "${var.stack_name}-${var.env}-app-sg"
  description       = "Allow application to communicate with other aws resources"
  vpc_id = var.vpc_id
  tags = merge(
  {
    "Name" = format("%s-%s-frontend-sg",var.stack_name,terraform.workspace),
  },
  var.tags,
  )
}