# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DEPLOY A SINGLE EC2 INSTANCE
# This template runs a simple "Hello, World" web server on a single EC2 Instance
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ----------------------------------------------------------------------------------------------------------------------
# REQUIRE A SUPPORTED TERRAFORM VERSION
# ----------------------------------------------------------------------------------------------------------------------

terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.0.0, < 7.0.0"
    }
  }
}

# ------------------------------------------------------------------------------
# CONFIGURE OUR AWS CONNECTION
# ------------------------------------------------------------------------------

provider "aws" {
  region = var.aws_region
}

data "aws_ssm_parameter" "al2023_ami" {
  count = var.ami_id == null ? 1 : 0

  name            = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
  with_decryption = false
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY A SINGLE EC2 INSTANCE
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_instance" "example" {
  ami = var.ami_id != null ? var.ami_id : data.aws_ssm_parameter.al2023_ami[0].insecure_value

  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.instance.id]

  user_data                   = <<-EOF
              #!/bin/bash
              mkdir -p /var/www/html
              echo "Hello, World" > /var/www/html/index.html
              nohup /usr/bin/python3 -m http.server "${var.server_port}" --directory /var/www/html >/var/log/terraform-example-http.log 2>&1 &
              EOF
  user_data_replace_on_change = true

  metadata_options {
    http_put_response_hop_limit = 1
    http_tokens                 = "required"
  }

  root_block_device {
    encrypted = true
  }

  tags = merge(var.resource_tags, {
    Name = "terraform-example"
  })
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE THE SECURITY GROUP THAT'S APPLIED TO THE EC2 INSTANCE
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_security_group" "instance" {
  name        = "terraform-example-instance"
  description = "Allow HTTP access to the Terraform example web server"

  dynamic "ingress" {
    for_each = length(var.allowed_cidr_blocks) == 0 ? [] : [var.allowed_cidr_blocks]

    content {
      description = "HTTP access to the example web server"
      from_port   = var.server_port
      to_port     = var.server_port
      protocol    = "tcp"
      cidr_blocks = ingress.value
    }
  }

  tags = merge(var.resource_tags, {
    Name = "terraform-example-instance"
  })
}
