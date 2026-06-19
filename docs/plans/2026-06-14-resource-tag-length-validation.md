# Resource Tag Length Validation

## Status: Completed

## Context

The module rejects empty, blank, and AWS-reserved resource tags but accepts
keys and values beyond EC2's documented 128- and 256-character limits. Those
inputs defer an avoidable failure to provider planning or resource creation.

## Priority

Medium plan-time reliability. Caller-controlled tags should fail at the
variable boundary before provider or AWS API interaction.

## Requirements

- Require every resource tag key to contain at most 128 Terraform characters.
- Require every resource tag value to contain at most 256 Terraform characters.
- Preserve non-empty maps, nonblank keys and values, and reserved `aws:` prefix
  rejection.
- Accept keys and values exactly at their documented limits.
- Add mocked Terraform plan tests for accepted boundaries and overlong values.
- Extend static contracts, maintained documentation, and completed evidence.

## Scope Boundaries

- Do not restrict the documented EC2 character set, tag count, default tags,
  resource merging, provider versions, or any AWS resource behavior.
- Do not run `terraform apply`, access real AWS credentials, or create state.

## Verification

- focused resource-tag mocked plans
- Terraform formatting, read-only initialization, validation, and full mocked
  test suite from repository and external directories
- hostile key-limit, value-limit, boundary-test, documentation, suite-count,
  and plan-status mutations
- provider-lock identity plus state, plan, variable, credential, artifact,
  secret, and exact-diff audits

## Verification Results

- Focused resource-tag mocked plans passed all eight boundary and rejection
  cases.
- The repository and external-directory `make check` passed Terraform
  formatting, read-only initialization, validation, and the full mocked suite.
- Six hostile resource-tag length mutations were rejected across key and value
  predicates, boundary coverage, maintained documentation, suite count, and
  completed-plan evidence.
- Provider-lock identity plus state, plan, variable, credential, artifact,
  secret, exact-diff, staged-path, and whitespace audits passed.

## Risks

- Terraform's `length` uses grapheme clusters while AWS documents Unicode
  characters in UTF-8; the provider remains authoritative for unusual Unicode
  edge cases.
