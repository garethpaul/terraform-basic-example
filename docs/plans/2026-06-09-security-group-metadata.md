# Security Group Metadata

## Status: Completed

## Context

The example security group exposed the configured HTTP port, but the AWS
resource and ingress rule depended on nearby Terraform comments to explain
their purpose. Plan output and AWS console views should carry that intent
directly, especially because the default ingress CIDR is intentionally public
for the demo.

## Objectives

- Add a security group description that explains the example web-server access.
- Add an ingress rule description for the HTTP exposure.
- Add a `Name` tag to the security group for AWS console visibility.
- Preserve the configurable port and CIDR behavior.
- Extend static checks to keep the metadata in place.

## Work Completed

- Added `description` to `aws_security_group.instance`.
- Added an ingress `description` for the HTTP rule.
- Added a `Name` tag to the security group.
- Extended `scripts/check-terraform-source.py` to require descriptions and the
  tag.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `make check`
- `git diff --check`

`terraform` is not installed in this environment, so `make check` reports that
`terraform fmt`, `terraform init`, and `terraform validate` were not run after
static verification passes.

## Follow-Up Candidates

- Add quickstart and destroy instructions to the README.
- Document expected AWS costs and required credentials.
