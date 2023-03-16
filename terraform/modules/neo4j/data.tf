

#define user data
data "template_cloudinit_config" "user_data" {
  gzip          = false
  base64_encode = false
  part {
    content = <<EOF
#cloud-config
---
users:
  - name: "${local.ssh_user}"
    gecos: "${local.ssh_user}"
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: wheel
    shell: /bin/bash
    ssh_authorized_keys:
    - "${data.aws_ssm_parameter.sshkey.value}"
EOF
  }

  part {
    content_type = "text/x-shellscript"
    content      = file("${path.module}/ssm.sh")
  }
}

data "aws_ssm_parameter" "amz_linux" {
  name = "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
}

#grab public ssh key
data "aws_ssm_parameter" "sshkey" {
  name = var.public_ssh_key_ssm_parameter_name
}

data "aws_iam_policy_document" "sts_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["ec2.amazonaws.com"]
      type        = "Service"
    }
  }
}
data "aws_iam_policy" "ssm_policy" {
  arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}


data "aws_security_group" "sg" {
  count = var.create_security_group ? 1 : 0
  id = var.db_security_group_id
}

data "aws_iam_instance_profile" "profile" {
  count = var.create_instance_profile ? 1 : 0
  name = var.db_iam_profile_name
}
