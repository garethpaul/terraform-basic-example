# Resource Tag Count Validation

## Status: Planned

## Context

Each managed resource merges a resource-owned `Name` tag into
`var.resource_tags`. The variable currently accepts 50 caller tags that omit
`Name`, producing 51 final EC2 tags and deferring a documented service-limit
failure to provider planning or the AWS API.

## Priority

Medium plan-time reliability. Validate the final merged tag-key set at the
module boundary so callers receive a deterministic Terraform variable error.

## Requirements

- Limit the final tag-key set, including the resource-owned `Name` key, to 50.
- Accept 49 caller tags that omit `Name`.
- Accept 50 caller tags when one key is already `Name` and will be overridden.
- Reject 50 caller tags that omit `Name` and therefore produce 51 final tags.
- Preserve nonempty-map, nonblank key/value, key/value length, reserved-prefix,
  default-tag, and resource-merge behavior.
- Add mocked plan regressions, fail-closed static contracts, maintained
  documentation, mutation coverage, and completed verification evidence.

## Scope Boundaries

- Do not change the resource-owned `Name` values or tag merge precedence.
- Do not restrict EC2 tag characters beyond existing validation.
- Do not run `terraform apply` against real infrastructure, access AWS
  credentials, create state, or change provider versions.

## Implementation Units

1. Validate the post-merge tag-key count in `variables.tf`.
2. Add exact-boundary mocked plans in `tests/resource_tags.tftest.hcl`.
3. Extend static contracts and maintained documentation.

## Verification

- focused resource-tag mocked plans
- repository and external-directory `make check`
- hostile count predicate, `Name` deduplication, boundary-test, documentation,
  suite-count, and plan-status mutations
- provider-lock identity plus state, plan, variable, credential, artifact,
  secret, exact-diff, staged-path, and whitespace audits

## Risks

- The two resources currently add only `Name`; future resource-owned tags must
  update this validation and its contracts together.
