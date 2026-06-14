# Changes

## 2026-06-14

- Added AMI ID length validation for the legacy 8-character and current
  17-character lowercase hexadecimal EC2 identifier widths.

## 2026-06-13

- Required canonical IPv4 CIDRs so host-bit-bearing ranges fail Terraform
  validation before reaching AWS security-group operations.
- Disabled inbound HTTP in the default plan and required callers to opt in
  with validated IPv4 CIDRs, with mocked provider runs for both states and
  rejection coverage for malformed and IPv6 ranges.

## 2026-06-12

- Rejected IPv6 ranges passed to the security group's IPv4-only ingress field
  and added a mocked Terraform plan test for the address-family boundary.
- Rejected empty, blank, and AWS-reserved common resource tags and added
  mocked Terraform plan tests for accepted defaults and invalid tag inputs.

## 2026-06-10

- Rejected fractional server ports and added mocked native Terraform plan tests
  for accepted defaults and expected variable-validation failures.
- Made Terraform validation independent of the caller's working directory and
  enforced read-only provider initialization, formatting diffs, and stable
  non-color validation output.
- Hardened CI with Ubuntu 24.04, concurrency cancellation, and version labels
  for commit-pinned actions.
- Extended static checks to require the reviewed AWS provider 6.49.0 lock,
  canonical and cross-platform checksums, and the immutable initialization
  path.
- Added a least-privilege GitHub Actions workflow that runs `make check` with
  Terraform 1.15.6, commit-pinned Node 24 actions, and disabled checkout
  credential persistence.
- Constrained Terraform to supported 1.x releases and the AWS provider to 6.x,
  with a checked-in provider lockfile for reproducible initialization.
- Made the Makefile's Terraform validation chain stop on the first failed
  formatting, initialization, or validation command.
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
