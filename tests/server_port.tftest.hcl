mock_provider "aws" {}

run "accept_default_server_port" {
  command = plan
}

run "reject_fractional_server_port" {
  command = plan

  variables {
    server_port = 8080.5
  }

  expect_failures = [var.server_port]
}
