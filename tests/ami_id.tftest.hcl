mock_provider "aws" {
  mock_data "aws_ssm_parameter" {
    defaults = {
      insecure_value = "ami-0123456789abcdef0"
    }
  }
}

run "accept_region_local_al2023_default" {
  command = apply

  assert {
    condition     = length(data.aws_ssm_parameter.al2023_ami) == 1
    error_message = "The default path must read the regional AL2023 public parameter."
  }

  assert {
    condition     = aws_instance.example.ami == "ami-0123456789abcdef0"
    error_message = "The default instance must use the mocked regional AL2023 AMI."
  }
}

run "accept_legacy_ami_id" {
  command = apply

  variables {
    ami_id = "ami-1234abcd"
  }

  assert {
    condition     = length(data.aws_ssm_parameter.al2023_ami) == 0
    error_message = "An explicit AMI override must bypass the public parameter lookup."
  }

  assert {
    condition     = aws_instance.example.ami == "ami-1234abcd"
    error_message = "The instance must preserve the explicit AMI override."
  }
}

run "accept_current_ami_id" {
  command = apply

  variables {
    ami_id = "ami-0fedcba9876543210"
  }

  assert {
    condition     = length(data.aws_ssm_parameter.al2023_ami) == 0
    error_message = "A current-width AMI override must bypass the public parameter lookup."
  }

  assert {
    condition     = aws_instance.example.ami == "ami-0fedcba9876543210"
    error_message = "The instance must preserve a current-width AMI override."
  }
}

run "reject_short_ami_id" {
  command = plan

  variables {
    ami_id = "ami-1234abc"
  }

  expect_failures = [var.ami_id]
}

run "reject_intermediate_length_ami_id" {
  command = plan

  variables {
    ami_id = "ami-123456789"
  }

  expect_failures = [var.ami_id]
}

run "reject_long_ami_id" {
  command = plan

  variables {
    ami_id = "ami-1234567890abcdef01"
  }

  expect_failures = [var.ami_id]
}

run "reject_uppercase_ami_id" {
  command = plan

  variables {
    ami_id = "ami-0C55B159CBFAFE1F0"
  }

  expect_failures = [var.ami_id]
}

run "reject_malformed_ami_id" {
  command = plan

  variables {
    ami_id = "image-0c55b159cbfafe1f0"
  }

  expect_failures = [var.ami_id]
}
