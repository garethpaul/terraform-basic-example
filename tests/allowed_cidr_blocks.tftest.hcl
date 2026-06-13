mock_provider "aws" {}

run "accept_private_default" {
  command = apply

  assert {
    condition     = length(aws_security_group.instance.ingress) == 0
    error_message = "The default configuration must not create an inbound HTTP rule."
  }
}

run "accept_explicit_ipv4_cidr_blocks" {
  command = apply

  variables {
    allowed_cidr_blocks = ["198.51.100.10/32"]
  }

  assert {
    condition     = length(aws_security_group.instance.ingress) == 1
    error_message = "Explicit IPv4 CIDRs must create one HTTP ingress block."
  }
}

run "reject_ipv6_cidr_blocks" {
  command = plan

  variables {
    allowed_cidr_blocks = ["2001:db8::/32"]
  }

  expect_failures = [var.allowed_cidr_blocks]
}

run "reject_malformed_cidr_blocks" {
  command = plan

  variables {
    allowed_cidr_blocks = ["not-a-cidr"]
  }

  expect_failures = [var.allowed_cidr_blocks]
}

run "reject_noncanonical_ipv4_cidr_blocks" {
  command = plan

  variables {
    allowed_cidr_blocks = ["198.51.100.10/24"]
  }

  expect_failures = [var.allowed_cidr_blocks]
}
