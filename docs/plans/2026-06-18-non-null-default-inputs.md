# Preserve Defaulted Inputs When Null Is Supplied

## Status: Completed

## Context

Terraform input variables are nullable unless a module says otherwise. In this
example, only `ami_id` intentionally uses `null` to select the region-local
Amazon Linux 2023 default AMI. The other defaulted inputs should not let an
explicit `null` erase the documented region, instance type, server port,
private ingress default, public IPv4 opt-in boundary, or ownership tags.

## Priority

Medium plan-time reliability. Make defaulted inputs fail closed against null
configuration while preserving the explicit nullable AMI override.

## Requirements

- Keep `ami_id` explicitly nullable so `null` continues to mean "use the
  region-local AL2023 default AMI."
- Mark `aws_region`, `instance_type`, `server_port`, `allowed_cidr_blocks`, and
  `resource_tags` non-nullable so explicit `null` cannot propagate into
  provider configuration, resource expressions, dynamic ingress, or tag merges.
- Add a mocked Terraform regression that sets each defaulted input to `null`
  and proves the defaults still govern the resulting resource values.
- Extend the static source contract so removing any non-nullable declaration or
  the null regression test fails `make check`.
- Do not add new inputs, change defaults, change AMI lookup behavior, run
  `terraform apply`, or contact AWS.

## Verification

- `PYTHON=/usr/bin/python3 scripts/check-terraform-source.py --mode config`
  rejected the missing non-nullable declarations before the variable fix.
- `PYTHON=/usr/bin/python3 make check`
  passed from the repository after the fix.
- `PYTHON=/usr/bin/python3 make -f "$PWD/Makefile" check`
  passed from an external directory after the fix.
- Terraform 1.15.6 was downloaded into the local worktree and verified against
  HashiCorp's SHA256SUMS file; `terraform fmt -check -diff` passed.
- Local `terraform init -backend=false -lockfile=readonly` could not install
  the AWS provider because the host filesystem had less than 1 GiB free and
  provider extraction failed with `no space left on device`; native
  provider-backed tests remain delegated to the hosted GitHub Actions check.
