
resource "aws_instance" "db" {
  ami                    = data.aws_ssm_parameter.amz_linux.value
  instance_type          = var.database_instance_type
  key_name               = var.ssh_key_name
  subnet_id              = var.db_subnet_id
  source_dest_check      = false
  vpc_security_group_ids =  [var.create_security_group ? aws_security_group.database_sg[0].id : data.aws_security_group.sg[0].id ]
  user_data              = data.template_cloudinit_config.user_data.rendered
  iam_instance_profile   = var.create_instance_profile ? aws_iam_instance_profile.db_profile[0].name : data.aws_iam_instance_profile.profile[0].name
  private_ip             = var.db_private_ip
  root_block_device {
    volume_type           = var.ebs_volume_type
    volume_size           = var.db_instance_volume_size
    delete_on_termination = true
    encrypted             = true

  }

  metadata_options {
    http_tokens = var.require_http_tokens
    http_endpoint = var.enable_http_endpoint
  }

  tags = merge(
    {
      "Name" = "${var.resource_prefix}-${var.database_name}",
    },
    var.tags,
  )
  lifecycle {
    ignore_changes = all
  }
}

#create boostrap script to hook up the node to ecs cluster
resource "aws_ssm_document" "ssm_neo4j_boostrap" {
  count   = var.create_bootstrap_script ? 1 : 0
  # name            = "${var.stack_name}-${var.env}-setup-database"
  name            = "${var.resource_prefix}-setup-database"
  document_type   = "Command"
  document_format = "YAML"
  content         = <<DOC
---
schemaVersion: '2.2'
description: State Manager Bootstrap Example
parameters: {}
mainSteps:
- action: aws:runShellScript
  name: configureDatabase
  inputs:
    runCommand:
    - set -ex
    - cd /tmp
    - rm -rf icdc-devops || true
    - yum -y install wget git python-setuptools python-pip
    - pip install --upgrade "pip < 21.0"
    - pip install ansible==2.8.0 boto boto3 botocore
    - git clone https://github.com/CBIIT/icdc-devops
    - cd icdc-devops/ansible && git checkout develop
    - ansible-playbook community-neo4j.yml
    - systemctl restart neo4j
DOC
  tags = merge(
    {
      "Name" = format("%s-%s", var.resource_prefix, "ssm-document")
    },
    var.tags,
  )
}

#create database security group
resource "aws_security_group" "database_sg" {
  count = var.create_security_group ? 1 : 0
  name = "${var.resource_prefix}-database-sg"
  description = "${var.resource_prefix} database security group"
  vpc_id = var.vpc_id
  tags = merge(
  {
    "Name" = format("%s-%s-%s",var.stack_name,var.env,"database-sg")
  },
  var.tags,
  )
}

resource "aws_ssm_association" "database" {
  name = var.create_bootstrap_script ? aws_ssm_document.ssm_neo4j_boostrap[0].name : data.aws_ssm_document.ssm[0].name
  targets {
    key    = "tag:Name"
    # values = ["${var.stack_name}-${var.env}-${var.database_name}"]
    values = ["${var.resource_prefix}-${var.database_name}-4"]
  }

  depends_on = [aws_instance.db]
}

resource "aws_iam_role" "db_role" {
  count = var.create_instance_profile ? 1 : 0
  name = "${var.resource_prefix}-database-instance-role"
  assume_role_policy = data.aws_iam_policy_document.sts_policy.json
  managed_policy_arns = [data.aws_iam_policy.ssm_policy.arn]
}

resource "aws_iam_instance_profile" "db_profile" {
  count = var.create_instance_profile ? 1 : 0
  role = aws_iam_role.db_role[0].name
  name = "${var.resource_prefix}-database-instance-profile"

}