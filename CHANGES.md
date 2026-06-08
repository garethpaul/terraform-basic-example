# Changes

## 2026-06-08

- Parameterized the AWS provider region and EC2 AMI ID with validated
  variables.
- Extended the static config checker to reject hardcoded provider region and
  instance AMI values in `main.tf`.
- Added a Makefile verification gate for Terraform hygiene and static
  configuration checks.
- Added Terraform state, local variable, and crash-log ignore rules.
- Declared the AWS provider source/version requirement.
- Added validation for `server_port` and made ingress CIDR blocks configurable.
- Documented the local verification workflow.
