# AMI ID Length Validation

## Status: Completed

## Context

The `ami_id` variable requires a lowercase hexadecimal `ami-` prefix but
accepts any suffix length. Values such as `ami-a` pass local validation even
though EC2 AMI identifiers use either the legacy 8-character or current
17-character hexadecimal width.

## Priority

Reject structurally impossible image identifiers during Terraform variable
validation, before provider or AWS API interaction.

## Requirements

- Accept lowercase hexadecimal AMI IDs with 8 or 17 suffix characters.
- Preserve the existing current-format default.
- Reject too-short, intermediate-length, too-long, uppercase, and malformed
  identifiers.
- Preserve region, instance type, port, CIDR, tags, metadata, encryption,
  immutable provider, and no-apply behavior.
- Add native mocked Terraform tests, fail-closed static contracts, and
  maintained documentation.

## Verification

- The focused static config contract passed with the two accepted AMI widths
  and five invalid identifier classes enforced.
- The repository and external-directory `make check` passed in an isolated
  Git-backed copy with Terraform 1.15.5, AWS provider 6.49.0, no cloud
  credentials, and 19 mocked plans passing with zero failures.
- Seven hostile AMI ID mutations were rejected: regex, short-ID, legacy-ID,
  current-ID, failure-count, documentation, and plan-status regressions.
- The hosted workflow remains authoritative for its pinned Terraform 1.15.6
  execution on the exact pushed head.
- State, plan, cache, variable, credential, artifact, and exact-diff audits
  passed before commit; only validation-created `.terraform` directories were
  removed by explicit path, and the provider lockfile remained unchanged.

## Scope Boundary

This change validates identifier shape only. It does not verify that an AMI
exists, belongs to the selected region or account, is trusted, or is currently
launchable.
