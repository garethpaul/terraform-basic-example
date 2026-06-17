# Make Public IPv4 Assignment Explicitly Opt In

## Status: Planned

## Context

The example already disables inbound HTTP when `allowed_cidr_blocks` is empty,
but `aws_instance.example` does not configure `associate_public_ip_address`.
AWS therefore inherits the selected subnet's auto-assign-public-IPv4 setting,
which can allocate a public address even though the default security group has
no ingress rule.

The AWS provider exposes `associate_public_ip_address` specifically to control
whether a VPC instance receives a public address. AWS also documents that this
launch setting overrides the subnet's default addressing behavior:

- <https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance.html>
- <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-ip-addresses.html>

## Priority

1. Make the default no-ingress configuration private at the EC2 network
   interface boundary, independent of subnet defaults.
2. Preserve the teaching example's public-address request when a caller
   explicitly supplies allowed IPv4 CIDRs, without claiming that this alone
   configures the subnet routing required for end-to-end reachability.
3. Prove both states with credential-free mocked Terraform tests and hostile
   static mutations.
4. Defer VPC, subnet, Elastic IP, NAT, load balancer, and DNS design; those
   would expand the repository beyond its single-instance teaching purpose.

## Requirements

- **R1:** `aws_instance.example` must set `associate_public_ip_address`
  explicitly instead of inheriting subnet behavior.
- **R2:** The empty `allowed_cidr_blocks` default must set public IPv4
  association to `false` and continue creating no ingress block.
- **R3:** A non-empty validated `allowed_cidr_blocks` list must set public IPv4
  association to `true` and continue creating one HTTP ingress block.
- **R4:** The exposure decision must derive from the existing ingress input;
  do not add a second boolean that can drift from security-group behavior.
- **R5:** Mocked Terraform tests must assert both resource values without AWS
  credentials, state persistence, or real infrastructure.
- **R6:** Static contracts and hostile mutations must reject omitted,
  unconditional, inverted, or input-independent public-IP assignment.
- **R7:** README, security guidance, vision, changelog, and the completed plan
  must explain that public address assignment and inbound HTTP are one explicit
  opt-in, while routing remains an external prerequisite.

## Technical Decisions

- Set `associate_public_ip_address` from whether
  `allowed_cidr_blocks` contains at least one entry. This keeps ingress and
  public addressing governed by one validated input and avoids contradictory
  combinations.
- Extend `tests/allowed_cidr_blocks.tftest.hcl` because that suite already owns
  the private-default and explicit-ingress contract. Do not introduce a second
  overlapping networking test file.
- Keep the current default VPC/subnet discovery behavior. Explicit subnet
  selection belongs in a broader networking example and is not necessary to
  override subnet public-IP defaults.
- Keep outputs unchanged. `public_ip` can remain empty for the private default
  and populated for the explicit public path.

## Implementation Units

### U1. Couple public addressing to ingress opt-in

- **Files:** `main.tf`
- **Outcome:** The instance receives no public IPv4 address by default and
  requests one only when validated ingress CIDRs are supplied.

### U2. Prove private and public resource plans

- **Files:** `tests/allowed_cidr_blocks.tftest.hcl`,
  `scripts/check-terraform-source.py`,
  `scripts/test_public_ip_assignment_contract.py`, `Makefile`
- **Outcome:** Mocked plans and static checks assert both branches, while
  isolated hostile mutations prove the guard cannot be removed or inverted.

### U3. Record the deterministic exposure boundary

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, `AGENTS.md`,
  `docs/plans/2026-06-17-public-ip-opt-in.md`
- **Outcome:** Operator guidance connects inbound CIDRs, public IPv4 cost, and
  routing prerequisites without implying that a real AWS apply was performed.

## Verification

- Run focused hygiene, configuration, and public-IP mutation contracts.
- Run Terraform formatting, read-only initialization, validation, and all
  mocked Terraform tests with the reviewed provider lock when the exact
  toolchain is available.
- Run `make check` from the repository and through the absolute Makefile path
  from an external directory.
- Audit the exact diff, lockfile digest, state/plan files, generated provider
  artifacts, Python bytecode, and credential patterns.
- Require one bounded exact-head hosted check snapshot after push.

## Scope Boundaries

- Do not run `terraform apply` or contact an AWS account.
- Do not add a VPC, subnet, route table, Internet gateway, Elastic IP, NAT
  gateway, load balancer, or DNS resource.
- Do not change provider versions, the AL2023 image selection, instance type,
  server port, metadata controls, encryption, tags, or existing outputs.
