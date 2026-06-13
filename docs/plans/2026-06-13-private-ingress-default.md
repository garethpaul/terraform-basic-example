# Private Ingress Default

Status: Completed

## Problem

The example validates that `allowed_cidr_blocks` contains IPv4 networks, but
its default still creates an HTTP ingress rule for `0.0.0.0/0`. A user who
applies the example without reviewing that variable exposes the demo server to
the public internet. The safer default is no inbound rule, with access enabled
only when the caller supplies reviewed IPv4 CIDRs.

## Requirements

- R1. Default `allowed_cidr_blocks` to an empty list so a default plan creates
  no HTTP ingress rule.
- R2. Create the existing described HTTP ingress block only when at least one
  validated IPv4 CIDR is supplied.
- R3. Continue rejecting IPv6 and malformed CIDRs before provider calls.
- R4. Add mocked Terraform runs for the empty default and explicit IPv4
  opt-in behavior.
- R5. Document how to opt in with a narrow caller-controlled CIDR.
- R6. Extend the static contract and hostile mutation checks so the private
  default and conditional rule cannot regress silently.

## Non-Goals

- Do not run `terraform plan` or `terraform apply` against a real AWS account;
  native tests may apply only against Terraform's mocked provider.
- Do not add IPv6 ingress, TLS termination, a load balancer, or VPC resources.
- Do not change the server port, AMI, instance type, provider lock, or workflow.

## Implementation

1. Change the ingress variable default and permit the empty safe state while
   retaining per-entry IPv4 validation.
2. Render the inline ingress block dynamically only for a non-empty list.
3. Expand native Terraform tests and the dependency-free checker contract.
4. Update user and security documentation with explicit opt-in guidance.

## Verification

- `python3 -B scripts/check-terraform-source.py --mode config` passed after the
  implementation and documentation updates.
- Terraform 1.15.6 formatting, read-only initialization with AWS provider
  6.49.0, validation, and credential-free mocked tests passed; 11 tests passed
  and 0 failed.
- Ten hostile mutations for the public default, conditional block, dynamic
  CIDR source, empty-list validation, native tests, documentation, and plan
  completion evidence were rejected with focused diagnostics.
- `TERRAFORM=/tmp/terraform-1.15.6 make check` passed the full hygiene,
  configuration, formatting, read-only initialization, validation, and 11-test
  mocked suite.
- The same full Make target passed from `/tmp`, confirming caller-directory
  independence.
- Final diff, artifact, secret-pattern, provider-lock, and worktree audits
  passed before commit; no state, variable, plan, credential, or provider
  artifact was selected for commit.
