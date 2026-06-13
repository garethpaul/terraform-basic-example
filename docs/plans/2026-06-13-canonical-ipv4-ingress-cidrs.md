# Canonical IPv4 Ingress CIDRs

## Status: Planned

## Context

The ingress variable now defaults to no inbound rule and rejects malformed or
IPv6 values. Terraform's IPv4 parser still accepts addresses with host bits,
such as `198.51.100.10/24`, while the AWS security-group API expects the
canonical network form `198.51.100.0/24`. Such input can pass local validation
and then fail only during a real provider operation.

## Priority

Reject noncanonical IPv4 ingress ranges during Terraform validation so the
read-only and mocked gates match the provider's apply-time input boundary.

## Requirements

- R1. Continue accepting an empty private default and canonical IPv4 CIDRs.
- R2. Reject IPv4 CIDRs whose host bits are not zero for their prefix length.
- R3. Preserve malformed and IPv6 rejection, explicit opt-in ingress, resource
  tags, metadata controls, encryption, and the no-apply policy.
- R4. Add a native mocked Terraform regression, fail-closed static contracts,
  hostile mutations, documentation, and full `make check` verification.

## Implementation Units

### Canonical network validation

**Files:** `variables.tf`, `tests/allowed_cidr_blocks.tftest.hcl`

Compare each IPv4 CIDR with Terraform's normalized zero-host network form and
expect validation failure for a noncanonical `/24` example.

### Contracts and maintenance record

**Files:** `scripts/check-terraform-source.py`, `README.md`, `SECURITY.md`,
`VISION.md`, `CHANGES.md`,
`docs/plans/2026-06-13-canonical-ipv4-ingress-cidrs.md`

Reject removed normalization, unsafe direct evaluation, missing negative test,
documentation drift, and regressed plan status.

## Verification Plan

- `/tmp/terraform-1.15.6 fmt -check -diff`
- `/tmp/terraform-1.15.6 init -backend=false -lockfile=readonly`
- `/tmp/terraform-1.15.6 validate -no-color`
- `/tmp/terraform-1.15.6 test -no-color`
- `TERRAFORM=/tmp/terraform-1.15.6 make check` locally and externally
- focused canonical-CIDR mutations
- lockfile identity, workflow/SVG parse, artifact, secret-pattern, and
  `git diff --check` audits

## Scope Boundaries

- Do not run `terraform plan` against a real account or `terraform apply`.
- Do not change the private default, create IPv6 ingress, normalize caller
  input silently, or alter AWS resources, provider versions, or workflow policy.
