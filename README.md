# terraform-basic-example

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/terraform-basic-example` is an infrastructure-as-code example. Create a basic terraform example

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Terraform (3).

## Repository Contents

- `README.md` - project overview and local usage notes
- `CHANGES.md` - maintenance history for Terraform guardrails
- `Makefile` - local verification entry points
- `docs/plans` - completed maintenance plans for the current baseline
- `main.tf` - Terraform provider and resource configuration
- `outputs.tf` - Terraform outputs
- `plans` - historical implementation notes
- `scripts` - static Terraform hygiene and configuration validators
- `SECURITY.md` - security reporting and disclosure guidance
- `variables.tf` - validated Terraform input variables
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: no top-level source directories detected
- Dependency and build manifests: none detected
- Entry points or build surfaces: none detected
- Test-looking files: no obvious test files detected

## Getting Started

### Prerequisites

- Git
- Terraform
- Python 3 for static repository checks

### Setup

```bash
git clone https://github.com/garethpaul/terraform-basic-example.git
cd terraform-basic-example
terraform init
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Use `terraform plan` after `terraform init` to inspect infrastructure changes before applying anything.
- Override `aws_region`, `ami_id`, and `instance_type` when planning outside
  the sample defaults; AMI IDs are region-specific and instance type changes
  can affect cost.
- Override `allowed_cidr_blocks` before real use if the example web server
  should not be reachable from the public internet. Values must be valid CIDR
  blocks.

## Testing and Verification

- `make check` runs static Terraform hygiene/configuration checks. When
  `terraform` is installed, the `build` target also runs `terraform fmt -check`,
  `terraform init -backend=false`, and `terraform validate`.
- Static checks require configurable region, AMI, instance type, ingress CIDR
  syntax, and server port validation instead of editing literals in `main.tf`.
  They also require the EC2 instance metadata service to use IMDSv2 tokens and
  a one-hop metadata response limit, the root block device to be encrypted, and
  user-data edits to replace the demo instance. Security group checks require
  descriptions and a `Name` tag so AWS plans show the rule intent.
- Hygiene checks also require completed canonical plans under `docs/plans`.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching infrastructure, proxy, cloud, or deployment configuration; examples from the scan include main.tf.

## Maintenance Notes

- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-terraform-basic-example-baseline.md` for the
  canonical Terraform hygiene and configuration baseline.
- See `docs/plans/2026-06-08-cidr-validation.md` for ingress CIDR validation
  coverage.
- See `docs/plans/2026-06-08-imdsv2-required.md` for the EC2 metadata token
  guard.
- See `docs/plans/2026-06-09-metadata-hop-limit.md` for the EC2 metadata hop
  limit guard.
- See `docs/plans/2026-06-09-root-volume-encryption.md` for the root volume
  encryption guard.
- See `docs/plans/2026-06-09-configurable-instance-type.md` for the EC2
  instance type variable guard.
- See `docs/plans/2026-06-09-user-data-replacement.md` for the EC2 user-data
  replacement guard.
- See `docs/plans/2026-06-09-security-group-metadata.md` for the security group
  description and tag guard.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
