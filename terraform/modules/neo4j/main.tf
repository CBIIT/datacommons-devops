
resource "aws_instance" "db" {
  ami                    = data.aws_ssm_parameter.amz_linux.value
  instance_type          = var.database_instance_type
  key_name               = var.ssh_key_name
  subnet_id              = var.db_subnet_id
  source_dest_check      = false
  vpc_security_group_ids =  [aws_security_group.database_sg.id ]
  user_data              = data.template_cloudinit_config.user_data.rendered
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
      "Name" = "${var.stack_name}-${var.env}-${var.database_name}",
    },
    var.tags,
  )
}

#create boostrap script to hook up the node to ecs cluster
resource "aws_ssm_document" "ssm_neo4j_boostrap" {
  name            = "${var.stack_name}-${var.env}-setup-database"
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
      "Name" = format("%s-%s", var.stack_name, "ssm-document")
    },
    var.tags,
  )
}

#create database security group
resource "aws_security_group" "database_sg" {
  name = "${var.stack_name}-${var.env}-database-sg"
  description = "${var.stack_name} ${var.env} database security group"
  vpc_id = var.vpc_id
  tags = merge(
  {
    "Name" = format("%s-%s-%s",var.stack_name,var.env,"database-sg")
  },
  var.tags,
  )
}

resource "aws_ssm_association" "database" {
  name = aws_ssm_document.ssm_neo4j_boostrap.name

  targets {
    key    = "tag:Name"
    values = ["${var.stack_name}-${var.env}-${var.database_name}-4"]
  }

  depends_on = [aws_instance.db]
}