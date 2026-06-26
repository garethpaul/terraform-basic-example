# Canonical Resource Tag Whitespace

## Status: Completed

## Context

The shared `resource_tags` validation rejects empty, overlong, reserved, and
excessive tag sets, but currently accepts keys and values with leading or
trailing whitespace. Those visually ambiguous tags can evade exact ownership,
cost, cleanup, and policy queries even though the intended text appears
correct in configuration review.

## Design

Require every caller-supplied tag key and value to equal its `trimspace`
result. Preserve internal spaces and the existing AWS-compatible character
surface; reject only surrounding whitespace instead of silently rewriting
caller input.

Add mocked Terraform failures for key and value boundaries, portable source
contracts for both predicates and both native tests, and hostile mutations
that remove each predicate independently.

## Work Completed

- Rejected leading or trailing whitespace in shared tag keys and values while
  preserving internal spaces and all existing canonical inputs.
- Added mocked Terraform rejection cases for both input boundaries.
- Added portable source requirements and six hostile resource-tag mutations
  covering merge propagation, validation predicates, and native cases.
- Updated the README, security posture, vision, and maintenance history.

## Verification

- The portable configuration contract failed before implementation for both
  missing predicates, both missing native cases, and the failure-count guard.
- `python3 scripts/test_resource_tag_contract.py` passed with six hostile
  resource-tag mutations rejected.
- Repository `/usr/bin/make check` passed all portable gates; Terraform was
  unavailable locally, so native format, initialization, validation, and
  mocked tests remain delegated to hosted CI.
- `git diff --check` passed.

## Scope Boundaries

- Resource creation, tag names and values, exposure, AMI selection, provider
  versions, state, outputs, and cost are unchanged for canonical inputs.
- No real AWS plan or apply will be run.
