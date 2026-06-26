# terraform-basic-example

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/terraform-basic-example` is an infrastructure-as-code example. Create a basic terraform example

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Terraform (3).

## Repository Contents

- `README.md` - project overview and local usage notes
- `CHANGES.md` - maintenance history for Terraform guardrails
- `.github/workflows/check.yml` - GitHub Actions baseline for `make check`
- `.terraform.lock.hcl` - reproducible AWS provider selection and checksums
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

- Terraform module: the root `main.tf`, `variables.tf`, and `outputs.tf` files define the deployment surface
- Dependency lock manifest: `.terraform.lock.hcl` pins the reviewed provider selection and checksums
- Verification entry points: `Makefile` and `.github/workflows/check.yml` run the repository gates
- Test suites: `tests/*.tftest.hcl` and `scripts/test_*.py` cover Terraform inputs and repository contracts

## Getting Started

### Prerequisites

- Git
- Terraform 1.5 or newer in the 1.x release line
- Python 3 for static repository checks
- An AWS account and credentials authorized to read the public Amazon Linux SSM
  parameter and manage the example EC2 instance, security group, and root volume
- A selected AWS region with a default VPC and default subnet behavior; this
  example does not declare its own VPC or subnet

### Setup

```bash
git clone https://github.com/garethpaul/terraform-basic-example.git
cd terraform-basic-example
terraform init
```

Use `terraform init -lockfile=readonly` after the first successful initialization
when you want to prove the checked-in AWS provider lock remains unchanged.

### Safe Credential Boundary

Prefer temporary credentials exposed through an AWS shared profile, SSO, or an
assumed role. For a configured profile:

```sh
export AWS_PROFILE=terraform-example
aws sts get-caller-identity
```

The AWS provider can read shared profiles and standard AWS environment
variables. Do not put AWS credentials in Terraform files, `.tfvars`, shell
history, commits, or pull requests. Environment credentials override profile
credentials, so clear stale `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and
`AWS_SESSION_TOKEN` values before relying on `AWS_PROFILE`.

Official references: [Terraform provider authentication](https://developer.hashicorp.com/terraform/tutorials/configuration-language/configure-providers)
and [AWS CLI configuration precedence](https://docs.aws.amazon.com/cli/latest/topic/config-vars.html).

### Cost Boundary

Applying the default plan creates one EC2 instance (`t2.micro` by default), its
encrypted root EBS volume, and one security group. Compute and provisioned EBS
storage can accrue charges even though default ingress and public IPv4
assignment are disabled. Data transfer can add charges when the instance is
reachable.

If `allowed_cidr_blocks` is non-empty, the instance also requests a public IPv4
address. As of June 26, 2026, AWS lists public IPv4 addresses at $0.005 per hour
(about $3.60 for a 30-day month) in addition to compute, storage, and transfer.
Prices, credits, taxes, instance availability, and Free Tier eligibility vary;
do not assume this example is free. Estimate the selected region and runtime in
the [AWS Pricing Calculator](https://calculator.aws/) and verify current
[EC2](https://aws.amazon.com/ec2/pricing/on-demand/),
[EBS](https://aws.amazon.com/ebs/pricing/), and
[public IPv4](https://aws.amazon.com/vpc/pricing/) pricing before applying.

### Architecture and AMI Boundary

The default SSM parameter resolves the latest regional Amazon Linux 2023
`x86_64` image. Keep the default or another x86-compatible instance type unless
you deliberately set `ami_id`. For an `arm64` instance type, supply a reviewed
regional arm64 AMI ID; changing only `instance_type` can produce an architecture
mismatch during planning or launch. Explicit `ami_id` overrides bypass the SSM
lookup, so the operator owns architecture, region, provenance, patch level, and
user-data compatibility.

## Running or Using the Project

### Safe Plan and Apply

Keep the plan artifact and the apply operation tied to the same reviewed input:

```sh
/usr/bin/make check
terraform init -lockfile=readonly
terraform plan -out=tfplan
terraform show tfplan
terraform apply tfplan
terraform output public_ip
```

Do not apply an unreviewed regenerated plan. With the private default,
`public_ip` is empty and the demo server is not reachable from the internet.

- The region-local Amazon Linux 2023 default AMI is resolved through AWS's
  public Systems Manager parameter. Set `ami_id` only for an architecture- or
  workload-specific image; explicit overrides bypass that lookup and retain
  structural validation. Override `aws_region` and `instance_type` as needed
  for availability and cost.
- Inbound HTTP and public IPv4 assignment are disabled by default. Set
  `allowed_cidr_blocks` explicitly to reviewed canonical IPv4 CIDRs when access
  is needed, preferably a narrow `/32` for the caller rather than `0.0.0.0/0`.
  For example, set
  `TF_VAR_allowed_cidr_blocks='["198.51.100.10/32"]'` before planning, replacing
  the reserved documentation address with the caller's public IP. This opts in
  to both settings; the selected subnet must still provide routing for
  end-to-end reachability, and a public IPv4 address may incur AWS charges.

### Restricting Ingress

Keep `allowed_cidr_blocks = []` unless internet access is required. If access is
required, prefer the caller's reviewed canonical `/32` and inspect the saved
plan for exactly one HTTP rule and one public IPv4 assignment. Avoid
`0.0.0.0/0`; it exposes the unauthenticated Python demo server to every IPv4
source and increases both security and cost risk.

### Destroy and Verify Cleanup

This example is intended to be short-lived. Review and apply a saved destroy
plan as soon as testing ends:

```sh
terraform plan -destroy -out=tfplan-destroy
terraform show tfplan-destroy
terraform apply tfplan-destroy
terraform state list
rm -f tfplan tfplan-destroy
```

After a successful destroy, `terraform state list` should contain no
`aws_instance.example` or `aws_security_group.instance` managed addresses.
Confirm the tagged instance, security group, and root volume are gone in the
selected AWS region; billing can continue for resources left outside the current
state or account/region. HashiCorp documents `terraform destroy` as the
interactive shortcut, but a saved destroy plan keeps review and execution tied
to the same proposed cleanup.

## Testing and Verification

- `make check` runs static Terraform hygiene/configuration checks. When
  `terraform` is installed, the `build` target also runs `terraform fmt
  -check -diff`, `terraform init -backend=false -lockfile=readonly`, and
  `terraform validate -no-color`, followed by mocked `terraform test
  -no-color` plans. The Makefile resolves paths from its own location, so the
  same check can be invoked from outside the repository. Verification also
  rejects caller-controlled roots, shells, startup makefiles, non-executing
  Make modes, and Make-syntax tool overrides; CI invokes `/usr/bin/make`
  directly. An executable workflow contract rejects 17 unsafe mutations to
  action pins, permissions, credentials, versions, triggers, and dispatch. A
  resource-tag contract separately rejects removal of either the instance or
  security-group ownership-tag merge.
- Native Terraform tests prove the default server port plans successfully and
  reject fractional port values before user data or security groups reach AWS.
- Defaulted inputs other than `ami_id` are non-nullable, so explicit `null`
  values preserve the documented defaults instead of propagating into provider
  configuration, network exposure decisions, or tag merges.
- AMI ID length validation accepts only the legacy 8-character or current
  17-character lowercase hexadecimal EC2 identifier widths.
- The region-local Amazon Linux 2023 default AMI uses `/usr/bin/python3` to
  serve the example page instead of relying on an obsolete image or BusyBox.
- Resource tag length validation rejects keys over 128 characters and values
  over 256 characters before provider planning.
- Resource tag count validation reserves the resource-owned `Name` key and
  rejects inputs that would produce more than 50 final EC2 tags.
- Resource tag whitespace validation rejects keys and values with leading or
  trailing whitespace so ownership, cleanup, cost, and policy matches remain
  exact; internal spaces remain supported.
- The instance applies validated shared ownership tags to its created EBS
  volumes at creation time, with a volume-specific `Name` tag for cleanup and
  cost traceability.
- Native Terraform tests use the mocked provider to prove the default creates
  no inbound HTTP rule, explicit canonical IPv4 CIDRs opt in to one rule, and
  malformed, IPv6, or host-bit-bearing ranges are rejected before they can
  reach the security group's IPv4-only `cidr_blocks` field.
- Static checks require configurable region, AMI, instance type, ingress CIDR
  syntax, and server port validation instead of editing literals in `main.tf`.
  Instance type validation requires EC2-shaped values such as `t2.micro`.
  Static checks also require the EC2 instance metadata service to use IMDSv2
  tokens and a one-hop metadata response limit, the root block device to be
  encrypted, and user-data edits to replace the demo instance. Security group
  checks require descriptions and a `Name` tag so AWS plans show the rule
  intent. Resource checks also require shared ownership tags to be merged into
  the EC2 instance, its created EBS volumes, and the security group.
- Hygiene checks also require completed canonical plans under `docs/plans`.
- GitHub Actions runs the same `make check` baseline on pushes and pull
  requests with Terraform 1.15.6, so formatting, provider initialization, and
  configuration validation are required in CI. The workflow uses read-only
  repository permissions, disabled checkout credential persistence, a fixed
  Ubuntu 24.04 image, a ten-minute timeout, concurrency cancellation, and
  commit-pinned Node 24 actions.
- `main.tf` constrains Terraform to supported 1.x releases and the AWS provider
  to 6.x. The validation gate treats `.terraform.lock.hcl` as read-only and
  currently requires the reviewed AWS provider 6.50.0 selection and registry
  checksums. Update the lockfile and static contract together when changing
  provider versions.

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
- See `docs/plans/2026-06-09-instance-type-syntax.md` for the EC2 instance type
  syntax validation guard.
- See `docs/plans/2026-06-09-user-data-replacement.md` for the EC2 user-data
  replacement guard.
- See `docs/plans/2026-06-09-security-group-metadata.md` for the security group
  description and tag guard.
- See `docs/plans/2026-06-09-resource-tags.md` for the shared resource
  ownership tag guard.
- See `docs/plans/2026-06-10-ci-baseline.md` for the reproducible Terraform
  validation gate.
- See `docs/plans/2026-06-10-readonly-provider-lock.md` for immutable provider
  lock enforcement.
- See `docs/plans/2026-06-10-server-port-integer-test.md` for whole-number port
  validation and the mocked Terraform plan test.
- See `docs/plans/2026-06-12-resource-tags-validation.md` for common tag input
  validation and mocked Terraform rejection tests.
- See `docs/plans/2026-06-12-ipv4-ingress-cidrs.md` for the ingress address-
  family boundary and mocked IPv6 rejection test.
- See `docs/plans/2026-06-13-private-ingress-default.md` for the opt-in HTTP
  ingress default and mocked rule-creation tests.
- See `docs/plans/2026-06-13-canonical-ipv4-ingress-cidrs.md` for canonical
  IPv4 CIDR validation before provider execution.
- See `docs/plans/2026-06-14-make-root-override-protection.md` for authoritative
  repository-root selection across all Make aliases.
- See `docs/plans/2026-06-14-ami-id-length-validation.md` for mocked plan
  coverage of accepted and structurally invalid EC2 image identifiers.
- See `docs/plans/2026-06-14-resource-tag-length-validation.md` for mocked
  EC2 tag boundary coverage.
- See `docs/plans/2026-06-14-resource-tag-count-validation.md` for mocked
  post-merge EC2 tag-count coverage.
- See `docs/plans/2026-06-15-aws-provider-lock-refresh.md` for the reviewed AWS
  provider 6.50.0 selection and canonical lock checksums.
- See `docs/plans/2026-06-17-al2023-default-ami.md` for the region-local Amazon
  Linux 2023 default AMI and explicit override behavior.
- See `docs/plans/2026-06-17-public-ip-opt-in.md` for deterministic public IPv4
  assignment coupled to the existing ingress opt-in.
- See `docs/plans/2026-06-18-non-null-default-inputs.md` for null-handling
  coverage on defaulted Terraform inputs.
- See `docs/plans/2026-06-21-make-authority-isolation.md` for the executable
  Make trust-boundary and adversarial root/flag/tool coverage.
- See `docs/plans/2026-06-25-instance-volume-tags.md` for created EBS volume
  ownership tag propagation and mocked plan coverage.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
