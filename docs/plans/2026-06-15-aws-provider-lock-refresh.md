# AWS Provider Lock Refresh

## Status: Planned

## Context

The module permits AWS provider 6.x, but the committed dependency lock still
selects 6.49.0. HashiCorp published AWS provider 6.50.0 on June 10, 2026, so
the reviewed lock and the fail-closed static contract are one patch release
behind the current compatible release.

## Priority

Medium dependency maintenance. Refresh the reproducible provider selection
while preserving the module's existing compatibility range and behavior.

## Requirements

- Select HashiCorp AWS provider 6.50.0 within the existing `>= 6.0.0, < 7.0.0`
  constraint.
- Regenerate canonical and cross-platform registry checksums with the pinned
  Terraform 1.15.6 toolchain.
- Update the static contract to reject a stale or unexpected provider
  selection.
- Keep read-only initialization, credential-free mocked tests, and the
  no-apply policy intact.
- Record completed verification evidence after implementation and tests pass.

## Scope Boundaries

- Do not change Terraform resources, variables, outputs, provider constraints,
  or workflow permissions.
- Do not access AWS credentials, create state, run a real plan, or apply
  infrastructure.
- Do not hand-edit registry checksums.

## Implementation Units

1. Regenerate `.terraform.lock.hcl` for AWS provider 6.50.0 with Terraform
   1.15.6.
2. Update the static provider-selection contract and maintained dependency
   documentation.
3. Run focused lock checks, full repository and external-directory gates, and
   hostile stale-version/checksum mutations.

## Verification

- Terraform 1.15.6 read-only initialization and mocked test suite
- repository-root and external-directory `make check`
- stale provider version, missing canonical checksum, insufficient registry
  checksum, writable-lock, and plan-status mutations
- exact diff, generated artifact, credential-pattern, and whitespace audits

## Source

- HashiCorp AWS provider 6.50.0 release:
  https://github.com/hashicorp/terraform-provider-aws/releases/tag/v6.50.0

## Completion Evidence

Pending implementation and validation.
