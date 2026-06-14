# AMI ID Length Validation

## Status: Planned

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

- focused static config contract and mocked Terraform tests
- repository and external-directory `make check`
- hostile regex, short-ID, legacy-ID, current-ID, failure-count,
  documentation, and plan-status mutations
- state, plan, cache, variable, credential, artifact, and exact-diff audits

## Scope Boundary

This change validates identifier shape only. It does not verify that an AMI
exists, belongs to the selected region or account, is trusted, or is currently
launchable.
