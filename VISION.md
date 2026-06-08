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
- Make AWS region, AMI, and open ingress explicit
- Avoid committing credentials or local state files

Next priorities:

- Add quickstart and destroy instructions to the README
- Document expected AWS costs and required credentials
- Parameterize region and AMI with safer defaults
- Add notes about restricting ingress beyond demo use

Contribution rules:

- One PR = one focused resource, variable, output, or documentation change.
- Do not commit state files, plans, credentials, or account IDs.
- Keep demo infrastructure small and easy to destroy.
- Explain any change that can increase cost or public exposure.

## Security And Responsible Use

The example creates public cloud resources and opens inbound HTTP. Users should
understand credentials, costs, public exposure, and teardown before applying it.

## What We Will Not Merge (For Now)

- Checked-in Terraform state or credentials
- Broad AWS architectures beyond the basic example
- Open management ports
- Cost-increasing resources without explicit rationale

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
