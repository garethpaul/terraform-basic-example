# Immutable Terraform Provider Lock

## Status: Completed

## Context

The repository committed an AWS provider lockfile, but routine validation used
plain `terraform init`. That allowed initialization to update dependency
selections instead of proving that the reviewed lockfile was complete and
usable. The Makefile also assumed it was invoked from the repository root, and
the hosted runner image could drift through the `ubuntu-latest` alias.

## Objectives

- Treat the committed provider lockfile as an immutable validation input.
- Detect provider version or checksum coverage drift before initialization.
- Keep local verification consistent from any working directory.
- Pin the hosted operating system and cancel superseded workflow runs.

## Work Completed

- Changed provider initialization to `terraform init -backend=false
  -lockfile=readonly`.
- Added formatting diffs and stable non-color validation output.
- Resolved Makefile paths from the Makefile location rather than the caller's
  current directory.
- Required the reviewed AWS provider 6.49.0 selection and constraint, a
  canonical package hash, and registry hashes for supported platforms in the
  static hygiene contract.
- Fixed CI to Ubuntu 24.04, added concurrency cancellation, and annotated each
  commit-pinned action with its verified release version.
- Updated repository documentation with the immutable lockfile contract.

## Verification

- `python3 -m py_compile scripts/check-terraform-source.py`
- `python3 scripts/check-terraform-source.py --mode hygiene`
- `python3 scripts/check-terraform-source.py --mode config`
- `make check`
- `make -C /path/to/terraform-basic-example check`
- Mutation checks for a floating runner, writable lockfile initialization,
  provider version drift, and missing registry checksums
- `git diff --check`

The validation path does not configure AWS credentials, plan infrastructure,
apply resources, or contact an AWS account.
