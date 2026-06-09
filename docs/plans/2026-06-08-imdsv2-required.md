# IMDSv2 Required

## Status: Completed

## Context

The example EC2 instance did not configure metadata service token behavior.
Even small teaching examples should prefer IMDSv2 so copied configurations do
not normalize token-optional instance metadata access.

## Objectives

- Preserve the single EC2 web-server example.
- Require IMDSv2 tokens on the instance metadata service.
- Add static checker coverage for the metadata option.
- Keep README, VISION, and CHANGES aligned with the new guard.

## Work Completed

- Added `metadata_options` with `http_tokens = "required"` to
  `aws_instance.example`.
- Extended `scripts/check-terraform-source.py --mode config` to require the
  IMDSv2 token setting.
- Added Python bytecode cache ignore rules for local checker validation.
- Updated repository maintenance documentation.

## Verification

- `python3 scripts/check-terraform-source.py --mode config`
- `python3 scripts/check-terraform-source.py --mode hygiene`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add README quickstart, cost, and `terraform destroy` cleanup instructions.
- Document region-specific AMI replacement steps before changing the default
  AMI.
