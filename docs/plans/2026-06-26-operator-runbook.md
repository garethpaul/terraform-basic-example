# Terraform Operator Runbook Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Document the safe credential, cost, AMI, ingress, apply, and destroy workflow for the checked-in AWS example.

**Architecture:** Preserve all Terraform resources, variables, tests, provider locks, and CI behavior. Add a source- and official-documentation-backed operator runbook with fail-closed documentation contracts, then retire only the four completed documentation roadmap items.

**Tech Stack:** Terraform 1.x, AWS provider 6.x, Markdown, Python 3, GNU Make, GitHub Actions

---

## Status: Completed

### Task 1: Add The Runbook Contract

**Files:**
- Modify: `scripts/check-terraform-source.py`
- Test: `scripts/check-terraform-source.py`

**Step 1: Write the failing test**

Require credentials, default-VPC assumptions, cost components, public IPv4 pricing, AMI architecture, ingress, saved plan/apply, output, destroy, roadmap, history, and completed-plan evidence.

**Step 2: Run test to verify it fails**

Run: `python3 scripts/check-terraform-source.py --mode hygiene`

Expected: FAIL because the current README does not contain the complete operator workflow.

### Task 2: Write The Operator Runbook

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`

**Step 1: Write minimal documentation**

Document temporary/profile credentials, default-VPC and IAM assumptions, current cost components, architecture-aligned AMI overrides, narrow ingress, saved plan/apply, output verification, and reviewed destroy cleanup.

**Step 2: Run focused contracts**

Run: `python3 scripts/check-terraform-source.py --mode hygiene`

Expected: PASS.

### Task 3: Prove Drift Fails Closed

**Files:**
- Test: `scripts/check-terraform-source.py`

**Step 1: Apply hostile mutations**

Mutate each new README, roadmap, history, and completed-plan contract in an isolated repository copy.

**Step 2: Verify each mutation fails**

Run the hygiene checker after each mutation.

Expected: every mutation is rejected.

### Task 4: Run The Full Gate

**Files:**
- Verify: `Makefile`

**Step 1: Run repository and external gates**

Run: `/usr/bin/make check`

Run: `cd "$(mktemp -d)" && /usr/bin/make -f /absolute/path/to/Makefile check`

Expected: static contracts, hostile mutations, native Terraform format/init/validate/tests, workflow policy, and Make authority gates pass.

### Task 5: Commit And Ship

**Files:**
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-operator-runbook.md`

**Step 1: Record exact validation**

Record mutation, local/external Terraform gates, official-source audit, review, hosted CI, and no-live-apply boundary evidence.

**Step 2: Commit**

```bash
git add README.md VISION.md CHANGES.md scripts/check-terraform-source.py docs/plans/2026-06-26-operator-runbook.md
git commit -m "docs: add Terraform operator runbook"
```

## Results

- The focused hygiene checker failed on the absent runbook and passed after the
  source-backed documentation reconciliation.
- All 26 isolated hostile runbook mutations were rejected.
- Checkout and external-directory `/usr/bin/make check` each passed 35 Make
  authority cases, 17 workflow mutations, six resource-tag mutations, five
  public-IPv4 mutations, hygiene checks, and configuration checks. Terraform
  was unavailable locally and skipped its native gates.
- Source claims were audited against `main.tf`, `variables.tf`, `.gitignore`,
  the pinned workflow, official AWS credential/VPC/EBS/EC2 pricing guidance,
  and official HashiCorp provider/plan/destroy documentation.
- No live AWS plan, apply, or destroy was executed.
