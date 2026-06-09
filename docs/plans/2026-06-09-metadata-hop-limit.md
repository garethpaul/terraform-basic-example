# Metadata Hop Limit

## Status: Completed

## Context

The example EC2 instance already requires IMDSv2 tokens. Because this is a
single-instance web-server demo rather than a container host, the instance
metadata response hop limit can also be explicit and narrow.

## Objectives

- Preserve the existing IMDSv2 token requirement.
- Limit metadata service HTTP PUT responses to one hop.
- Extend static checks so the metadata hop-limit guard is not removed.

## Work Completed

- Added `http_put_response_hop_limit = 1` to the EC2 `metadata_options` block.
- Kept `http_tokens = "required"` aligned in the same block.
- Extended `scripts/check-terraform-source.py` to require the hop-limit
  setting.
- Documented the metadata hop-limit guard in README, VISION, and CHANGES.

## Verification

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
