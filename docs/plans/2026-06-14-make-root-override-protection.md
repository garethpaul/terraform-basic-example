# Make Root Override Protection

## Status: Planned

## Context

The Makefile derives Terraform validation paths from its own location, but a
caller can replace `ROOT` through the environment or command line. That can
redirect static checks and read-only Terraform validation away from the
checked-out configuration.

## Priority

Infrastructure verification paths are a trust boundary. The repository must
select its own root while preserving explicit Python and Terraform executable
overrides and the existing no-apply posture.

## Objectives

- Protect the repository-derived root from caller assignments.
- Preserve the established root-first ordering and both tool overrides.
- Preserve all aliases, read-only initialization, validation, tests, and apply
  prohibition.
- Exercise every alias from repository and external working directories under
  hostile environment and command-line root values.
- Add mutation-sensitive source, README, and completed-plan contracts.

## Implementation Units

### U1. Protect the validation root

**Files:** `Makefile`

Mark the root declaration as an explicit GNU Make override without changing
tool variables, targets, or Terraform commands.

### U2. Preserve infrastructure safety contracts

**Files:** `scripts/check-terraform-source.py`, `README.md`

Require one root assignment total, the exact protected declaration, root-first
tool ordering, alias graph, read-only root-anchored commands, README indexing,
and this plan's completed evidence.

## Verification

- Hygiene/config and full `make check` gates without credentials.
- Repository/external working directories and hostile root assignments.
- Declaration, duplicate, placement, alias, path, README, and plan mutations.
- Provider-lock byte identity, apply prohibition, exact diff, protected
  Terraform/workflow paths, artifacts, secrets, and whitespace audits.
- Exact-head hosted Terraform 1.15.6 verification.

## Scope Boundary

This change does not alter Terraform configuration, tests, provider versions,
the lockfile, workflow policy, resources, ingress behavior, or execute plan or
apply.
