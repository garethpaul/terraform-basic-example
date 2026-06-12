mock_provider "aws" {}

run "accept_default_ipv4_cidr_blocks" {
  command = plan
}

run "reject_ipv6_cidr_blocks" {
  command = plan

  variables {
    allowed_cidr_blocks = ["2001:db8::/32"]
  }

  expect_failures = [var.allowed_cidr_blocks]
}
