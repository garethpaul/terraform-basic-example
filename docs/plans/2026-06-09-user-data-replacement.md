# User Data Replacement Guard

## Status: Completed

## Context

The example EC2 instance uses launch-time `user_data` to start the "Hello,
World" web server. If that script changes after an instance already exists, the
demo should create a fresh instance so the running server matches the checked-in
configuration.

## Objectives

- Preserve the single-instance EC2 example.
- Make user-data changes replace the demo instance.
- Extend static checks so future edits do not remove the replacement guard.

## Work Completed

- Added `user_data_replace_on_change = true` to `aws_instance.example`.
- Extended `scripts/check-terraform-source.py` to require the user-data
  replacement setting.
- Updated README, VISION, and CHANGES with the new launch-script guard.

## Verification

- Negative check before implementation:
  `python3 scripts/check-terraform-source.py --mode config` failed with
  `aws_instance.example must replace on user_data changes`.
- `python3 scripts/check-terraform-source.py --mode config`
- `python3 scripts/check-terraform-source.py --mode hygiene`
- `make check`
- `make verify`
- `git diff --check`

## Terraform Notes

Terraform was not installed in this environment, so provider initialization and
`terraform validate` were not run here. The repository `make check` wrapper
still runs `terraform fmt -check`, `terraform init -backend=false`, and
`terraform validate` when Terraform is available locally.
