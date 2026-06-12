# Terraform Basic Example CI Baseline

## Status: Completed

## Context

`terraform-basic-example` has static hygiene and configuration checks behind
`make check`. The repository needs a lightweight GitHub Actions gate so state
hygiene, metadata, tag, and security defaults are checked before review.

## Objectives

- Run the existing static Terraform baseline in GitHub Actions.
- Keep the hosted runner job useful even when the Terraform CLI is absent.
- Make the CI workflow presence part of the hygiene contract.

## Work Completed

- Added `.github/workflows/check.yml` to run `make check` on pushes, pull
  requests, and manual dispatches.
- Set up Python 3.12 in CI for the static Terraform checker.
- Extended hygiene checks to require the CI workflow and this completed plan.
- Updated README, VISION, SECURITY, and CHANGES with the CI baseline.

## Verification

- `make check`
- `git diff --check`

## Follow-Up Candidates

- Install a pinned Terraform CLI in CI once the desired version constraint is
  documented.
