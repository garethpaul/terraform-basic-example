# AGENTS.md

## Repository purpose

`garethpaul/terraform-basic-example` is an infrastructure-as-code example. Create a basic terraform example

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `main.tf` - Terraform configuration
- `outputs.tf` - Terraform configuration
- `variables.tf` - Terraform configuration
- `plans` - repository source or sample assets

## Development commands

- Install dependencies: `terraform init -backend=false`
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Terraform (3).
- Format Terraform with `terraform fmt`; use validation/plan only, never apply infrastructure from an agent session.

## Testing guidance

- Native Terraform tests live under `tests/`; treat `make check` as the minimum baseline.
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.
- Preserve the region-local Amazon Linux 2023 public-parameter default and keep
  explicit `ami_id` overrides query-free.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-terraform-basic-example-baseline.md` for the canonical Terraform hygiene and configuration baseline.
- See `docs/plans/2026-06-08-cidr-validation.md` for ingress CIDR validation coverage.
- See `docs/plans/2026-06-08-imdsv2-required.md` for the EC2 metadata token guard.
- Do not run `terraform apply` from an agent session; stop at format, validate, and plan-style review unless explicitly authorized.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
