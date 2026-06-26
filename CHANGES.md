# Changes

## 2026-06-26 04:04 PDT - P2 - Add the safe operator runbook

### Summary

Completed all four Terraform operator-documentation priorities with a
source-backed runbook for credentials, default-network assumptions, cost,
AMI architecture, ingress, saved apply plans, and reviewed cleanup.

### Work completed

- Documented temporary/profile credential use and AWS credential precedence.
- Listed the security-group resource plus the EC2, EBS, optional IPv4, and
  transfer cost surface without promising Free Tier eligibility or a
  region-independent bill.
- Documented the x86_64 default SSM image and explicit arm64 override boundary.
- Added saved plan/apply, output, narrow ingress, saved destroy, state, and
  account/region cleanup verification steps.
- Added fail-closed runbook, roadmap, history, and completed-plan contracts.

### Threads

- Started: none; the cohesive documentation work was handled directly.
- Continued: none.
- Stopped: none.

### Files changed

- `README.md` — added the complete operator runbook and official references.
- `VISION.md` — retired the four completed documentation priorities.
- `scripts/check-terraform-source.py` — added runbook drift contracts.
- `docs/plans/2026-06-26-operator-runbook.md` — recorded the implementation plan.
- `CHANGES.md` — recorded this cycle and its validation.

### Validation

- Initial hygiene checker — failed on the absent runbook contracts as expected.
- Focused hygiene checker — passed after the runbook reconciliation.
- Hostile runbook suite — rejected all 26 isolated README, roadmap, history,
  and completed-plan mutations.
- Checkout and external-directory `/usr/bin/make check` — each passed 35 Make
  authority cases, 17 workflow mutations, six resource-tag mutations, five
  public-IPv4 mutations, hygiene checks, and configuration checks. Terraform
  was unavailable locally, so native format/init/validate/test was skipped.
- Source audit — matched the one-instance/one-security-group resource surface,
  x86_64 SSM default, ingress/public-IP coupling, encrypted root volume, and
  default-network assumption to checked-in Terraform.
- Official-source audit — matched credential precedence and provider
  authentication to AWS/HashiCorp documentation, current public IPv4 pricing to
  AWS VPC pricing, and saved destroy-plan behavior to Terraform documentation.
- Pricing arithmetic — confirmed `$0.005 * 24 * 30 = $3.60` for the explicitly
  qualified 30-day public-IPv4 estimate.
- `git diff --check` — passed; no resource, variable, provider, test, lock, or
  workflow behavior changed.
- Hosted native Terraform, CodeQL, and exact-head review remain pending until
  the PR head is available.

### Bugs / findings

- P2: the previous README omitted required AWS permissions, default-VPC
  dependence, complete cost components, AMI architecture matching, saved apply
  plans, and a reviewable destroy workflow.

### Blockers

- No live AWS plan, apply, or destroy is executed from this maintenance session;
  account-specific permissions, pricing, networking, and cleanup remain operator
  responsibilities.

### Next action

- Require exact-head hosted Terraform and CodeQL gates before merge, then run
  the same gates on the merge commit.

## 2026-06-25

- Added resource tag whitespace validation so leading or trailing whitespace
  cannot create visually ambiguous ownership, cleanup, cost, or policy keys.
- Added mocked Terraform failures and portable hostile mutations for both tag
  key and value boundaries.
- Propagated validated shared ownership tags to the EC2 instance's created EBS
  volumes with a volume-specific `Name` tag for cleanup and cost traceability.
- Added mocked Terraform and portable source contracts for default and custom
  volume tag propagation.

## 2026-06-21

- Isolated repository verification from caller-controlled Make roots, shells,
  startup files, non-executing modes, and Make-syntax tool overrides.
- Added adversarial Make authority regression coverage and pinned GitHub
  Actions verification to `/usr/bin/make`.

## 2026-06-17

- Coupled EC2 public IPv4 assignment to the existing validated ingress opt-in,
  keeping the no-ingress default independent of subnet auto-assignment settings.
- Replaced the obsolete region-specific image default with the latest
  region-local Amazon Linux 2023 default AMI and an override-safe public
  parameter lookup, using the AL2023 system Python server for the demo page.
- Marked all non-AMI defaulted inputs non-nullable so explicit `null` values
  cannot erase the documented defaults for region, instance type, port,
  ingress, public IPv4 assignment, or ownership tags.

## 2026-06-15

- Refreshed the reproducible AWS provider lock to 6.50.0 and tightened static
  validation around the reviewed canonical and cross-platform checksums.

## 2026-06-14

- Added resource tag count validation that reserves the resource-owned `Name`
  key and rejects final EC2 tag sets above 50 entries.
- Added resource tag length validation for EC2's 128-character key and
  256-character value limits.
- Added AMI ID length validation for the legacy 8-character and current
  17-character lowercase hexadecimal EC2 identifier widths.

## 2026-06-13

- Required canonical IPv4 CIDRs so host-bit-bearing ranges fail Terraform
  validation before reaching AWS security-group operations.
- Disabled inbound HTTP in the default plan and required callers to opt in
  with validated IPv4 CIDRs, with mocked provider runs for both states and
  rejection coverage for malformed and IPv6 ranges.

## 2026-06-12

- Rejected IPv6 ranges passed to the security group's IPv4-only ingress field
  and added a mocked Terraform plan test for the address-family boundary.
- Rejected empty, blank, and AWS-reserved common resource tags and added
  mocked Terraform plan tests for accepted defaults and invalid tag inputs.

## 2026-06-10

- Rejected fractional server ports and added mocked native Terraform plan tests
  for accepted defaults and expected variable-validation failures.
- Made Terraform validation independent of the caller's working directory and
  enforced read-only provider initialization, formatting diffs, and stable
  non-color validation output.
- Hardened CI with Ubuntu 24.04, concurrency cancellation, and version labels
  for commit-pinned actions.
- Extended static checks to require the reviewed AWS provider 6.49.0 lock,
  canonical and cross-platform checksums, and the immutable initialization
  path.
- Added a least-privilege GitHub Actions workflow that runs `make check` with
  Terraform 1.15.6, commit-pinned Node 24 actions, and disabled checkout
  credential persistence.
- Constrained Terraform to supported 1.x releases and the AWS provider to 6.x,
  with a checked-in provider lockfile for reproducible initialization.
- Made the Makefile's Terraform validation chain stop on the first failed
  formatting, initialization, or validation command.
- Extended hygiene checks to require the CI workflow and completed CI plan.

## 2026-06-09

- Added common `resource_tags` and static checks so the EC2 instance and
  security group carry ownership/cleanup metadata.
- Tightened `instance_type` variable validation so obvious non-EC2-looking
  values fail before provider planning.
- Added security group and ingress descriptions plus a `Name` tag so the demo
  network exposure is visible in Terraform plans and AWS.
- Made EC2 user-data edits replace the demo instance and added static guard
  coverage.
- Limited EC2 instance metadata responses to one hop and added static guard
  coverage.
- Moved the EC2 instance type into a validated `instance_type` variable while
  keeping the `t2.micro` default.
- Extended static configuration checks to reject hardcoded instance type
  literals in `main.tf`.
- Enabled encryption on the EC2 instance root block device.
- Extended static Terraform checks to require root volume encryption.

## 2026-06-08

- Required IMDSv2 tokens on the EC2 example and added static checker coverage.
- Ignored Python bytecode caches produced by local checker syntax validation.
- Added validation for `allowed_cidr_blocks` and static checker coverage for
  ingress CIDR syntax.
- Added `make check` as the shared repository verification alias.
- Parameterized the AWS provider region and EC2 AMI ID with validated
  variables.
- Extended the static config checker to reject hardcoded provider region and
  instance AMI values in `main.tf`.
- Added a Makefile verification gate for Terraform hygiene and static
  configuration checks.
- Added Terraform state, local variable, and crash-log ignore rules.
- Declared the AWS provider source/version requirement.
- Added validation for `server_port` and made ingress CIDR blocks configurable.
- Documented the local verification workflow.
- Added canonical `docs/plans` coverage and made hygiene checks require
  completed plans.
