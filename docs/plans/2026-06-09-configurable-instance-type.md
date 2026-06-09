# Configurable Instance Type Guard

## Status: Completed

## Context

The example EC2 instance kept its size as a literal `t2.micro` value in
`main.tf`. That default is appropriate for a small demo, but users should be
able to review and override the instance type without editing resource
definitions, especially because instance type changes affect cost and regional
availability.

## Objectives

- Preserve the existing `t2.micro` default.
- Move instance type selection into a validated Terraform variable.
- Extend static checks so future changes do not reintroduce a literal
  `instance_type` in `main.tf`.

## Work Completed

- Added `variable "instance_type"` with a non-empty validation rule.
- Changed `aws_instance.example` to use `var.instance_type`.
- Extended `scripts/check-terraform-source.py` to require the variable-backed
  instance type.
- Updated README, VISION, and CHANGES with the new configuration guard.

## Verification

- `python3 scripts/check-terraform-source.py --mode config`
- `make lint`
- `make test`
- `make build`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Document expected monthly cost ranges for the default instance and common
  alternatives.
- Add a sample `terraform.tfvars.example` with safe placeholders if the example
  grows beyond a single instance.
