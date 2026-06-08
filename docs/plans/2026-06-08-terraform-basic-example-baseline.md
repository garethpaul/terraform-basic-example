# Terraform Basic Example Baseline

## Status: Completed

## Context

`terraform-basic-example` is a small AWS EC2 web-server teaching example. The
maintenance baseline should keep the configuration easy to understand while
making state hygiene, public ingress, region, AMI, and port assumptions explicit
before anyone runs `terraform apply`.

## Objectives

- Preserve the single-instance Terraform example.
- Keep generated state, local variables, crash logs, and credentials out of git.
- Require configurable AWS region, AMI, ingress CIDRs, and server port
  validation.
- Run static hygiene and configuration checks through `make check`.
- Maintain completed maintenance plans under `docs/plans`.

## Work Completed

- Confirmed `make check` runs hygiene, configuration, and optional Terraform
  CLI validation checks.
- Added canonical `docs/plans` coverage for the current Terraform baseline.
- Extended hygiene checks to require completed `docs/plans` entries with
  `make check` verification.
- Updated README, VISION, and CHANGES to make the baseline discoverable.

## Verification

- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add quickstart, cost, and destroy instructions to the README.
- Run `terraform fmt -check`, `terraform init -backend=false`, and
  `terraform validate` where Terraform is installed.
