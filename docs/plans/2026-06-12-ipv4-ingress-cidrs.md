# IPv4 Ingress CIDRs

## Status: Completed

## Context

`allowed_cidr_blocks` accepts every value parsed by Terraform's `cidrhost`,
including IPv6 ranges. The security-group ingress rule passes those values only
to the AWS provider's `cidr_blocks` field, which is the IPv4 field; IPv6 values
therefore cross the module input boundary and fail later in provider handling.

## Priority

Reject address-family mismatches at the variable boundary so callers receive a
deterministic configuration error before provider planning.

## Requirements

- R1. Continue requiring one or more syntactically valid CIDR values.
- R2. Reject IPv6 CIDRs while ingress uses the IPv4-only `cidr_blocks` field.
- R3. Preserve existing IPv4 defaults and configurable ingress behavior.
- R4. Add a mocked Terraform plan test that expects the IPv6 input failure.
- R5. Add static contracts, hostile mutations, documentation, and full
  `make check` verification without credentials, plan, or apply.

## Scope Boundaries

- Do not add an IPv6 ingress field or change the default public demo range.
- Do not create, plan, or apply AWS infrastructure.
- Do not change provider versions, the lockfile, or hosted workflow.

## Implementation Units

### Input and executable contract

**Files:** `variables.tf`, `tests/allowed_cidr_blocks.tftest.hcl`,
`scripts/check-terraform-source.py`

- Require every allowed CIDR to pass Terraform's structured IPv4 CIDR parser.
- Exercise the default and an expected IPv6 validation failure with a mocked
  AWS provider.

### Maintenance record

**Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
`docs/plans/2026-06-12-ipv4-ingress-cidrs.md`

## Verification Plan

- static hygiene and configuration checks
- locked Terraform `fmt`, read-only `init`, `validate`, and mocked `test`
- `make check` from the repository and an external directory
- focused IPv6-validation mutations
- `git diff --check`

## Verification Record

- `python3 -B scripts/check-terraform-source.py --mode config` passed with the
  IPv4 validation and mocked-test contracts enabled.
- Terraform 1.15.6 `fmt -check -diff` and `git diff --check` passed.
- Five focused mutations were rejected: removing or neutralizing the IPv4
  guard, removing the IPv6 rejection run, replacing its fixture with IPv4, and
  removing the expected variable-validation failure.
- Exact Terraform 1.15.6 `make check` passed hygiene, configuration, formatting,
  read-only AWS 6.49.0 initialization, validation, and all nine mocked plans.
  The provider lockfile remained byte-identical and no credentials, plan, or
  apply were used.
- External-directory `make -f /absolute/path/Makefile check` passed the same
  pinned gate, confirming caller-directory independence.

## Remaining Risks

- Mocked plans do not prove behavior in a live AWS account.
- Supporting IPv6 later requires a separate `ipv6_cidr_blocks` input and rule.
