# Resource Tags

## Status: Completed

## Context

The example already tagged the EC2 instance and security group with resource
names. For infrastructure examples, shared ownership and cleanup metadata makes
plans easier to review and helps users identify demo resources after applying
the configuration.

## Objectives

- Preserve the existing per-resource `Name` tags.
- Add common tags that can be overridden by users.
- Apply common tags to both the EC2 instance and security group.
- Add static coverage so future resource changes keep ownership tags visible.

## Work Completed

- Added a `resource_tags` map variable with `ManagedBy` and `Project` defaults.
- Merged `resource_tags` into the EC2 instance tags while preserving the
  instance `Name`.
- Merged `resource_tags` into the security group tags while preserving the
  security group `Name`.
- Extended `scripts/check-terraform-source.py --mode config` to require common
  tags and per-resource `Name` tags.
- Updated README, VISION, and CHANGES notes for shared resource tags.

## Verification

- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `make lint`
- `make check`
- `make verify`
- `git diff --check`

`terraform` is not installed in this environment, so `make check` reports that
the Terraform CLI validation was not run after static verification passes.
