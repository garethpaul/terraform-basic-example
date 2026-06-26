# Security Policy

## Supported Versions

The supported security scope for `terraform-basic-example` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: Create a basic terraform example

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/terraform-basic-example` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be an Infrastructure-as-code example. The active security scope is the code and documentation on the default branch.
- Review found infrastructure, deployment, proxy, or cloud configuration; changes in those areas should receive security-focused review before merge.
- Provider selections and checksums are committed in `.terraform.lock.hcl`;
  CI initializes with `-lockfile=readonly`, and static checks require the
  reviewed provider selection plus canonical and cross-platform registry
  checksums. Review lockfile changes alongside the corresponding constraint.
- GitHub Actions runs `make check` with Terraform 1.15.6, read-only repository
  permissions, disabled checkout credential persistence, a fixed Ubuntu 24.04
  image, a ten-minute timeout, concurrency cancellation, and commit-pinned Node
  24 actions; review workflow and checker changes alongside Terraform
  configuration changes.
- Mocked Terraform tests reject fractional listener ports before invalid user
  data or security-group values can reach an AWS plan.
- Defaulted inputs other than the intentional `ami_id` override are
  non-nullable, preventing explicit `null` values from erasing the reviewed
  region, instance type, listener port, private ingress default, public IPv4
  boundary, or ownership tags.
- AMI ID length validation rejects structurally impossible image identifiers
  before provider or AWS API interaction.
- The region-local Amazon Linux 2023 default AMI is read from an AWS-owned
  public parameter; explicit AMI overrides bypass the lookup and remain
  structurally validated.
- Resource tag length validation rejects overlong keys and values before
  provider or AWS API interaction.
- Resource tag count validation includes the resource-owned `Name` key and
  rejects final EC2 tag sets above the 50-tag service limit.
- Resource tag whitespace validation rejects leading or trailing whitespace
  instead of creating visually ambiguous ownership and policy identifiers.
- Validated shared ownership tags are applied when the instance's EBS volumes
  are created, keeping storage visible for cleanup and cost attribution.
- Ingress validation requires canonical IPv4 CIDRs and rejects IPv6,
  malformed, or host-bit-bearing ranges before they reach the AWS security
  group's IPv4-only `cidr_blocks` field.
- The default plan creates no inbound HTTP rule; callers must opt in with
  reviewed IPv4 CIDRs, preferably a narrow source range rather than public
  `0.0.0.0/0` access.
- The shared Makefile may initialize, validate, and test Terraform, but the
  static contract rejects `terraform apply`.

## Infrastructure Notes

For infrastructure examples, report overly permissive access controls, exposed secrets, insecure defaults, unsafe network rules, or configurations that could mislead users into deploying vulnerable systems. Do not attempt to access real cloud resources that are not yours.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

The default Terraform inputs request neither inbound HTTP nor a public IPv4
address. Supplying `allowed_cidr_blocks` opts in to both settings; restrict the
CIDRs to trusted callers, confirm the selected subnet's routing separately, and
account for public IPv4 charges before applying the example.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
