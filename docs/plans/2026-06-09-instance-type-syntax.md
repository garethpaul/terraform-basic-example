# Instance Type Syntax Guard

## Status: Completed

## Context

The example already exposed `instance_type` as a variable, but its validation
only rejected empty strings. That still allowed obvious non-EC2-looking values
to reach `terraform plan`, where the provider would report the error later.

## Objectives

- Preserve the default `t2.micro` sample instance type.
- Validate that custom values look like EC2 instance type identifiers.
- Keep the validation broad enough for instance families with hyphens.
- Add static coverage so the syntax guard remains in place.

## Work Completed

- Replaced the non-empty `instance_type` validation with an EC2-shaped regex.
- Updated the validation error message to show a concrete example value.
- Extended `scripts/check-terraform-source.py` to require the syntax guard.
- Extended hygiene checks to require this completed plan.
- Updated README, VISION, and CHANGES.

## Verification

- Negative: `make test` failed before the Terraform fix because
  `instance_type` only checked for non-empty input.
- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `make check`
- `make verify`
- `git diff --check`

`terraform` is not installed in this environment, so `make check` reports that
the Terraform CLI validation was not run after static verification passes.

## Follow-Up Candidates

- Document expected AWS costs for common instance type overrides.
- Add provider-backed validation on a machine with Terraform installed.
