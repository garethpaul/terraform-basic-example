# Configurable Region And AMI

## Problem

The example declared a configurable ingress CIDR and port, but the AWS provider
region and EC2 AMI ID were still hardcoded in `main.tf`. Users planning outside
`us-east-2` had to edit the source file directly, and AMI IDs are
region-specific.

## TDD Evidence

1. Extended `scripts/check-terraform-source.py --mode config` to reject
   hardcoded provider region and instance AMI values.
2. Added validated `aws_region` and `ami_id` variables with the existing sample
   defaults.
3. Updated `main.tf` to read the provider region and instance AMI from those
   variables.

## Verification

- `make lint`
- `make test`
- `make verify`
- `git diff --check`

`make build` runs `terraform fmt -check`, `terraform init -backend=false`, and
`terraform validate` when Terraform is installed; otherwise static checks run.
