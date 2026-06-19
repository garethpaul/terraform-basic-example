# Reproducible Terraform Validation Gate

## Status: Completed

## Context

The repository had static configuration checks behind `make check`, but no
hosted gate. The initial CI draft only installed Python, which meant the
Makefile would skip `terraform fmt`, provider initialization, and `terraform
validate`. Terraform and AWS provider constraints were also broad enough for
substantial toolchain drift between contributors.

## Objectives

- Run the complete `make check` baseline on pushes and pull requests.
- Pin the hosted Terraform CLI and provider dependency selection.
- Keep workflow permissions least-privilege and execution bounded.
- Enforce the CI and lockfile contract with the static hygiene checker.

## Work Completed

- Added `.github/workflows/check.yml` for pushes to `master`, pull requests,
  and manual runs.
- Installed Terraform 1.15.6 with an immutable Node 24 action commit.
- Granted only read access to repository contents, disabled checkout credential
  persistence, and set a ten-minute timeout.
- Constrained Terraform to `>= 1.5.0, < 2.0.0` and the AWS provider to the 6.x
  release line.
- Generated and committed `.terraform.lock.hcl` for reproducible provider
  selection and checksum verification.
- Extended hygiene and configuration checks to enforce the workflow,
  constraints, and lockfile.
- Made the Makefile's Terraform command chain fail immediately so an earlier
  formatting or initialization error cannot be hidden by a later command.
- Updated README, SECURITY, VISION, and CHANGES with the validation contract.

## Verification

- `python3 -m py_compile scripts/check-terraform-source.py`
- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `terraform fmt -check`
- `terraform init -backend=false`
- `terraform validate`
- `make check`
- `git diff --check`

The validation gate initializes providers but does not configure AWS
credentials, create a plan, apply infrastructure, or contact an AWS account.
The static contract also rejects `terraform apply` in the shared Makefile.
