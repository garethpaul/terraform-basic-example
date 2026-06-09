## Terraform Basic Example Vision

Terraform Basic Example is a small Terraform configuration that launches one
AWS EC2 instance running a simple "Hello, World" web server.

The repository is useful as a minimal infrastructure-as-code teaching example:
it shows provider configuration, a security group, user data, variables, and
outputs without adding module complexity.

The goal is to keep the example easy to understand while making cloud cost,
security, and teardown expectations explicit.

The current focus is:

Priority:

- Preserve the single-instance web server example
- Keep Terraform version assumptions visible
- Make AWS region, AMI, instance type, and open ingress explicit and configurable
- Validate ingress CIDR inputs before Terraform plans reach AWS
- Require IMDSv2 tokens on the example EC2 instance
- Keep EC2 metadata response hop limits explicit for the single-instance demo
- Keep the example instance root volume explicitly encrypted
- Replace the demo instance when its launch-time user data changes
- Avoid committing credentials or local state files
- Keep completed maintenance plans under `docs/plans`

Next priorities:

- Add quickstart and destroy instructions to the README
- Document expected AWS costs and required credentials
- Document region-specific AMI selection and safer demo defaults
- Add notes about restricting ingress beyond demo use

Contribution rules:

- One PR = one focused resource, variable, output, or documentation change.
- Do not commit state files, plans, credentials, or account IDs.
- Keep demo infrastructure small and easy to destroy.
- Explain any change that can increase cost or public exposure.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The example creates public cloud resources and opens inbound HTTP. Users should
understand credentials, costs, public exposure, and teardown before applying it.

## What We Will Not Merge (For Now)

- Checked-in Terraform state or credentials
- Broad AWS architectures beyond the basic example
- Open management ports
- Loose EC2 metadata response hop limits without rationale
- Unencrypted EC2 root volumes
- Cost-increasing resources without explicit rationale

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
