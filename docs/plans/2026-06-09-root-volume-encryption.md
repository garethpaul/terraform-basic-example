# Root Volume Encryption

## Status: Completed

## Context

The Terraform example already requires IMDSv2 and validates public ingress
inputs, but the EC2 instance root volume did not make encryption explicit. Even
for a small teaching example, declaring encryption keeps the security posture
visible in the configuration instead of relying on account defaults.

## Objectives

- Keep the single-instance example easy to read.
- Explicitly encrypt the EC2 root block device.
- Extend local static checks so the encryption guard is not accidentally
  removed.

## Work Completed

- Added an encrypted `root_block_device` block to `aws_instance.example`.
- Extended `scripts/check-terraform-source.py` to require root volume
  encryption.
- Updated README, VISION, and CHANGES with the root volume guard.

## Verification

- `python3 scripts/check-terraform-source.py --mode config`
- `python3 scripts/check-terraform-source.py --mode hygiene`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add teardown and cost notes before encouraging real AWS applies.
- Document safer non-public ingress defaults for users adapting the example.
