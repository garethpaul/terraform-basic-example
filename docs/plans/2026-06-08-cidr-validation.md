# Ingress CIDR Validation

## Status: Completed

## Context

The example made ingress CIDR blocks configurable, but Terraform accepted any
string list before planning. Invalid CIDR values would fail later in provider
validation, and the static checker did not preserve input validation for this
public network surface.

## Objectives

- Preserve the single-instance web server example.
- Keep `allowed_cidr_blocks` configurable for demo and safer local use.
- Validate ingress CIDR syntax before provider calls.
- Extend static checks so the validation stays in place.

## Work Completed

- Added Terraform validation for one or more valid `allowed_cidr_blocks`
  entries.
- Extended `scripts/check-terraform-source.py --mode config` to require CIDR
  validation.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add README examples for private office/VPN CIDR overrides.
- Document expected AWS costs and `terraform destroy` cleanup steps.
