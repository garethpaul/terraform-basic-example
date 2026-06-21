# Make Authority Isolation

Status: Completed

## Goal

Keep the repository's verification entry points authoritative when invoked
from another directory or with hostile Make variables, flags, startup files,
shell overrides, and tool paths containing shell metacharacters.

## Changes

- Resolve and export the repository root from the checked-in Makefile alone.
- Freeze trusted Python and Terraform executable overrides as literal values.
- Fix the recipe shell, reject non-executing/error-ignoring Make modes, and
  reject caller-supplied `MAKEFLAGS`, `MAKEFILES`, and `MAKEFILE_LIST`.
- Add a self-contained adversarial root harness across every public target and
  an executable workflow contract covering 17 unsafe mutations.
- Invoke the hosted gate through `/usr/bin/make` and enforce that workflow in
  the static repository contract.

## Verification

- repository and external-directory `make check` passed
- 35 target/authority combinations passed with quoted and literal-dollar tool
  paths
- 17 unsafe workflow mutations were rejected
- raw Make-syntax tool values, root/shell overrides, startup boundaries, and
  non-executing/error-ignoring modes were rejected
- `git diff --check` and strict repository integrity checks passed
