mock_provider "aws" {
  mock_data "aws_ssm_parameter" {
    defaults = {
      insecure_value = "ami-0123456789abcdef0"
    }
  }
}

run "accept_explicit_nulls_as_defaulted_inputs" {
  command = apply

  variables {
    aws_region          = null
    instance_type       = null
    server_port         = null
    allowed_cidr_blocks = null
    resource_tags       = null
    ami_id              = null
  }

  assert {
    condition     = aws_instance.example.ami == "ami-0123456789abcdef0"
    error_message = "The nullable AMI override should keep using the regional AL2023 default when set to null."
  }

  assert {
    condition     = aws_instance.example.instance_type == "t2.micro"
    error_message = "An explicit null instance_type must resolve to the default instance type."
  }

  assert {
    condition     = aws_instance.example.associate_public_ip_address == false
    error_message = "Explicit null allowed_cidr_blocks must preserve the private default."
  }

  assert {
    condition     = length(aws_security_group.instance.ingress) == 0
    error_message = "Explicit null allowed_cidr_blocks must not create inbound HTTP."
  }

  assert {
    condition     = aws_instance.example.tags.ManagedBy == "terraform"
    error_message = "Explicit null resource_tags must preserve the default ownership tags."
  }
}
