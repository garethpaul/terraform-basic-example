mock_provider "aws" {}

run "accept_default_current_ami_id" {
  command = plan
}

run "accept_legacy_ami_id" {
  command = plan

  variables {
    ami_id = "ami-1234abcd"
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
