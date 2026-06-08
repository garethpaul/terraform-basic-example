# Terraform Static Gate

## Problem

The Terraform example had no repo-local verification command, no ignore rules
for generated state or local variable files, no provider source declaration, and
a hard-coded open ingress CIDR. The `server_port` variable also lacked bounds
validation.

## TDD Evidence

1. Added `scripts/check-terraform-source.py` and Makefile targets.
2. Ran `make lint` and confirmed missing Terraform hygiene patterns.
3. Ran `make test` and confirmed missing provider/CIDR/validation contracts.
4. Updated Terraform config and docs, then reran the full verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `git diff --check`
