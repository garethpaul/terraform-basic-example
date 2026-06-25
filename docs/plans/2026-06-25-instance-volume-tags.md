# Instance Volume Tags

## Status: Completed

## Context

The EC2 instance and security group carried validated ownership tags, but the
encrypted root EBS volume did not. HashiCorp's AWS provider documentation says
instance tags are not applied to root or additional EBS volumes, while
`volume_tags` applies uniform tags during volume creation. Untagged storage is
harder to attribute, audit, and clean up independently in AWS inventory and
billing views.

## Design

Merge the existing validated `resource_tags` map into `volume_tags` on the
single `aws_instance`, overriding only `Name` with
`terraform-example-volume`. This preserves the existing tag validation and
50-tag post-merge boundary while giving storage a resource-specific identity.

Use `volume_tags` rather than post-creation `root_block_device.tags` so tags are
present during volume creation and remain compatible with tag-based creation
policies. The example does not manage any volume through a separate
`aws_ebs_volume` resource, so the provider's conflict warning does not apply.

## Work Completed

- Added creation-time shared ownership tags for the instance's EBS volumes.
- Added mocked plan assertions for default and caller-supplied ownership tags.
- Added a portable source contract that rejects missing or detached volume tag
  propagation.
- Added a mutation test that distinguishes ordinary resource `tags` from
  `volume_tags` and rejects removal of either existing ownership-tag merge.
- Updated the security, vision, README, and change records.

## Verification

- `python3 scripts/check-terraform-source.py --mode config`
- `python3 scripts/test_resource_tag_contract.py`
- `/usr/bin/make check`
- `git diff --check`
- Native `terraform test` is delegated to hosted CI because Terraform is not
  installed in the local environment.

## Provider Evidence

- HashiCorp AWS provider `aws_instance` tag guide:
  https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance
- AWS EC2 resource tagging guidance:
  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html

## Scope Boundaries

- Provider versions, encryption, volume sizing and type, instance replacement,
  network exposure, user data, outputs, and input validation are unchanged.
- No infrastructure was planned against a real AWS account or applied.
