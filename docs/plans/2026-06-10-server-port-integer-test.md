# Server Port Integer Test

## Status: Completed

## Context

The `server_port` variable used Terraform's `number` type and a range check.
That accepted fractional values such as `8080.5`, even though BusyBox and AWS
security-group port fields require whole numbers. The failure therefore
surfaced later than the repository's input-validation boundary.

## Work Completed

- Required `server_port` to equal its floored value in addition to remaining
  within the valid TCP port range.
- Added native Terraform tests with a mocked AWS provider for the accepted
  default and expected fractional-input failure.
- Added `terraform test -no-color` to the locked initialization and validation
  gate.
- Extended static checks to preserve the validation and executable test cases.

## Verification

- `make check`
- `terraform test -no-color`
- Negative validation and test-source mutations
- `git diff --check`

The test uses a mocked provider and does not configure AWS credentials, contact
an AWS account, or create infrastructure.
