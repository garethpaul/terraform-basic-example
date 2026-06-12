# Changes

## 2026-06-10

- Added a lightweight GitHub Actions workflow that runs `make check` for the
  Terraform hygiene and configuration baseline.
- Extended hygiene checks to require the CI workflow and completed CI plan.

## 2026-06-09

- Added common `resource_tags` and static checks so the EC2 instance and
  security group carry ownership/cleanup metadata.
- Tightened `instance_type` variable validation so obvious non-EC2-looking
  values fail before provider planning.
- Added security group and ingress descriptions plus a `Name` tag so the demo
  network exposure is visible in Terraform plans and AWS.
- Made EC2 user-data edits replace the demo instance and added static guard
  coverage.
- Limited EC2 instance metadata responses to one hop and added static guard
  coverage.
- Moved the EC2 instance type into a validated `instance_type` variable while
  keeping the `t2.micro` default.
- Extended static configuration checks to reject hardcoded instance type
  literals in `main.tf`.
- Enabled encryption on the EC2 instance root block device.
- Extended static Terraform checks to require root volume encryption.

## 2026-06-08

- Required IMDSv2 tokens on the EC2 example and added static checker coverage.
- Ignored Python bytecode caches produced by local checker syntax validation.
- Added validation for `allowed_cidr_blocks` and static checker coverage for
  ingress CIDR syntax.
- Added `make check` as the shared repository verification alias.
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
- Added canonical `docs/plans` coverage and made hygiene checks require
  completed plans.
