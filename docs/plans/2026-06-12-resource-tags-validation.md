# Resource Tag Validation

## Status: Completed

## Context

The example applies caller-provided tags to both AWS resources, but the
`resource_tags` variable previously accepted an empty map, blank keys or
values, and AWS-reserved `aws:` keys. Those inputs either removed the ownership
metadata used for cleanup or deferred an avoidable failure to provider
planning.

## Objectives

- Reject unusable common tags at the Terraform variable boundary.
- Preserve the existing default ownership and cleanup metadata.
- Exercise accepted and rejected inputs with native Terraform tests.
- Protect the validation and test cases with the static repository contract.

## Work Completed

- Required at least one common resource tag.
- Required every tag key and value to remain non-blank after trimming.
- Rejected case-insensitive use of the AWS-reserved `aws:` key prefix.
- Added mocked Terraform plan tests for the accepted defaults and each rejected
  input class.
- Extended the static checker to require the variable rules, native tests, and
  this completed plan.
- Updated repository guidance and change history with the validation contract.

## Verification

- `python3 -m py_compile scripts/check-terraform-source.py`
- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `make check`
- Mutations removing each tag rule or native rejection case
- `git diff --check`

The native tests use a mocked provider and do not configure AWS credentials,
contact an AWS account, or create infrastructure.
