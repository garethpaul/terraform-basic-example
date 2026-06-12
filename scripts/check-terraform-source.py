#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-terraform-basic-example-baseline.md"
SECURITY_GROUP_PLAN = DOCS_PLANS / "2026-06-09-security-group-metadata.md"
INSTANCE_TYPE_SYNTAX_PLAN = DOCS_PLANS / "2026-06-09-instance-type-syntax.md"
RESOURCE_TAGS_PLAN = DOCS_PLANS / "2026-06-09-resource-tags.md"
CI_PLAN = DOCS_PLANS / "2026-06-10-ci-baseline.md"
LOCK_ENFORCEMENT_PLAN = DOCS_PLANS / "2026-06-10-readonly-provider-lock.md"
SERVER_PORT_TEST_PLAN = DOCS_PLANS / "2026-06-10-server-port-integer-test.md"
RESOURCE_TAGS_VALIDATION_PLAN = DOCS_PLANS / "2026-06-12-resource-tags-validation.md"
IPV4_INGRESS_PLAN = DOCS_PLANS / "2026-06-12-ipv4-ingress-cidrs.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"
LOCK_FILE = ROOT / ".terraform.lock.hcl"
SERVER_PORT_TEST = ROOT / "tests" / "server_port.tftest.hcl"
RESOURCE_TAGS_TEST = ROOT / "tests" / "resource_tags.tftest.hcl"
ALLOWED_CIDR_BLOCKS_TEST = ROOT / "tests" / "allowed_cidr_blocks.tftest.hcl"
EXPECTED_WORKFLOW = """name: Check

on:
  push:
    branches:
      - master
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  check:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false

      - name: Set up Python
        uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6.2.0
        with:
          python-version: "3.12"

      - name: Set up Terraform
        uses: hashicorp/setup-terraform@dfe3c3f87815947d99a8997f908cb6525fc44e9e # v4.0.1
        with:
          terraform_version: "1.15.6"
          terraform_wrapper: false

      - name: Run baseline
        run: make check
"""


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def tracked_files():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return [], f"unable to inspect tracked files: {result.stderr.strip()}"
    return result.stdout.splitlines(), None


def hygiene_checks():
    errors = []
    if not CANONICAL_PLAN.exists():
        errors.append("docs/plans/2026-06-08-terraform-basic-example-baseline.md is missing")
    if not SECURITY_GROUP_PLAN.exists():
        errors.append("docs/plans/2026-06-09-security-group-metadata.md is missing")
    if not INSTANCE_TYPE_SYNTAX_PLAN.exists():
        errors.append("docs/plans/2026-06-09-instance-type-syntax.md is missing")
    if not RESOURCE_TAGS_PLAN.exists():
        errors.append("docs/plans/2026-06-09-resource-tags.md is missing")
    if not CI_PLAN.exists():
        errors.append("docs/plans/2026-06-10-ci-baseline.md is missing")
    if not LOCK_ENFORCEMENT_PLAN.exists():
        errors.append("docs/plans/2026-06-10-readonly-provider-lock.md is missing")
    if not SERVER_PORT_TEST_PLAN.exists():
        errors.append("docs/plans/2026-06-10-server-port-integer-test.md is missing")
    if not RESOURCE_TAGS_VALIDATION_PLAN.exists():
        errors.append("docs/plans/2026-06-12-resource-tags-validation.md is missing")
    if not IPV4_INGRESS_PLAN.exists():
        errors.append("docs/plans/2026-06-12-ipv4-ingress-cidrs.md is missing")
    if not SERVER_PORT_TEST.exists():
        errors.append("tests/server_port.tftest.hcl is missing")
    if not RESOURCE_TAGS_TEST.exists():
        errors.append("tests/resource_tags.tftest.hcl is missing")
    if not ALLOWED_CIDR_BLOCKS_TEST.exists():
        errors.append("tests/allowed_cidr_blocks.tftest.hcl is missing")

    plans = sorted(DOCS_PLANS.glob("*.md")) if DOCS_PLANS.exists() else []
    if not plans:
        errors.append("docs/plans must contain at least one completed plan")
    for plan_path in plans:
        plan = plan_path.read_text(encoding="utf-8")
        if "Status: Completed" not in plan or "make check" not in plan:
            errors.append(f"{plan_path.relative_to(ROOT)} must record completed status and make check verification")

    gitignore = read_text(".gitignore") if (ROOT / ".gitignore").exists() else ""
    gitignore_lines = {line.strip() for line in gitignore.splitlines()}
    for pattern in (".terraform/", "*.tfstate", "*.tfstate.*", "*.tfvars", "crash.log"):
        if pattern not in gitignore_lines:
            errors.append(f".gitignore must include Terraform pattern: {pattern}")

    tracked, tracked_error = tracked_files()
    if tracked_error:
        errors.append(tracked_error)
    for path in tracked:
        if path.endswith(".tfstate") or ".tfstate." in path or path.endswith(".tfvars"):
            errors.append(f"state or local variable file must not be tracked: {path}")

    if not CI_WORKFLOW.exists():
        errors.append(".github/workflows/check.yml is missing")
    else:
        workflow = CI_WORKFLOW.read_text(encoding="utf-8")
        if workflow != EXPECTED_WORKFLOW:
            errors.append("CI workflow must match the reviewed credential-free Terraform validation contract")

    if not LOCK_FILE.exists():
        errors.append(".terraform.lock.hcl is missing")
    else:
        lock_file = LOCK_FILE.read_text(encoding="utf-8")
        if 'provider "registry.terraform.io/hashicorp/aws"' not in lock_file:
            errors.append(".terraform.lock.hcl must pin the hashicorp/aws provider")
        if 'version     = "6.49.0"' not in lock_file:
            errors.append(".terraform.lock.hcl must select the reviewed AWS provider 6.49.0")
        if 'constraints = ">= 6.0.0, < 7.0.0"' not in lock_file:
            errors.append(
                ".terraform.lock.hcl must preserve the reviewed AWS provider constraint"
            )
        if not re.search(r'^\s+"h1:[A-Za-z0-9+/=]+",$', lock_file, re.MULTILINE):
            errors.append(
                ".terraform.lock.hcl must include a canonical provider package checksum"
            )
        if len(re.findall(r'^\s+"zh:[0-9a-f]{64}",$', lock_file, re.MULTILINE)) < 10:
            errors.append(".terraform.lock.hcl must include registry checksums for supported platforms")

    for doc_path in ("README.md", "SECURITY.md", "VISION.md", "CHANGES.md"):
        if "GitHub Actions" not in read_text(doc_path):
            errors.append(f"{doc_path} must document the GitHub Actions check")

    makefile = read_text("Makefile")
    if re.search(
        r'(?:terraform|"?\$\(TERRAFORM\)"?)\s+apply\b',
        makefile,
        re.IGNORECASE,
    ):
        errors.append("Makefile must not apply infrastructure")
    if 'set -e;' not in makefile:
        errors.append("Makefile Terraform validation must fail immediately when a command fails")
    for fragment in (
        "ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))",
        'cd "$(ROOT)";',
        "fmt -check -diff",
        "init -backend=false -lockfile=readonly",
        "validate -no-color",
        "test -no-color",
    ):
        if fragment not in makefile:
            errors.append(f"Makefile is missing expected validation fragment: {fragment}")

    return errors


def config_checks():
    errors = []
    main = read_text("main.tf")
    variables = read_text("variables.tf")
    server_port_test = read_text("tests/server_port.tftest.hcl") if SERVER_PORT_TEST.exists() else ""
    resource_tags_test = read_text("tests/resource_tags.tftest.hcl") if RESOURCE_TAGS_TEST.exists() else ""
    allowed_cidr_blocks_test = (
        read_text("tests/allowed_cidr_blocks.tftest.hcl")
        if ALLOWED_CIDR_BLOCKS_TEST.exists()
        else ""
    )

    if 'required_version = ">= 1.5.0, < 2.0.0"' not in main:
        errors.append("main.tf must constrain Terraform to the supported 1.x range")
    if "required_providers" not in main or 'source  = "hashicorp/aws"' not in main:
        errors.append("main.tf must declare the hashicorp/aws provider source")
    if 'version = ">= 6.0.0, < 7.0.0"' not in main:
        errors.append("main.tf must constrain the AWS provider to the supported 6.x range")
    if 'region = "us-east-2"' in main:
        errors.append("provider region must be configurable")
    if "region = var.aws_region" not in main:
        errors.append("provider region must reference var.aws_region")
    if re.search(r'ami\s+=\s+"ami-[0-9a-f]+"', main):
        errors.append("instance AMI must be configurable")
    if "ami                    = var.ami_id" not in main:
        errors.append("instance AMI must reference var.ami_id")
    if re.search(r'instance_type\s+=\s+"[^"]+"', main):
        errors.append("instance type must be configurable")
    if not re.search(r'instance_type\s+=\s+var\.instance_type', main):
        errors.append("instance type must reference var.instance_type")
    if 'cidr_blocks = ["0.0.0.0/0"]' in main:
        errors.append("security group ingress must use configurable CIDR blocks")
    if "cidr_blocks = var.allowed_cidr_blocks" not in main:
        errors.append("security group ingress must reference var.allowed_cidr_blocks")
    if 'description = "Allow HTTP access to the Terraform example web server"' not in main:
        errors.append("security group must describe the example web server access")
    if 'description = "HTTP access to the example web server"' not in main:
        errors.append("security group ingress must describe the exposed HTTP rule")
    if main.count("tags = merge(var.resource_tags, {") < 2:
        errors.append("EC2 instance and security group must merge common resource tags")
    if 'Name = "terraform-example"' not in main:
        errors.append("EC2 instance must carry a Name tag")
    if 'Name = "terraform-example-instance"' not in main:
        errors.append("security group must carry a Name tag")
    if 'variable "allowed_cidr_blocks"' not in variables:
        errors.append("variables.tf must define allowed_cidr_blocks")
    if "var.allowed_cidr_blocks" not in variables or "can(cidrnetmask(cidr))" not in variables:
        errors.append("allowed_cidr_blocks must validate IPv4 CIDR values")
    if 'length(regexall(":", cidr)) == 0' in variables:
        errors.append("allowed_cidr_blocks must use Terraform IPv4 parsing instead of string heuristics")
    for fragment in (
        'mock_provider "aws" {}',
        'run "accept_default_ipv4_cidr_blocks"',
        'run "reject_ipv6_cidr_blocks"',
        'allowed_cidr_blocks = ["2001:db8::/32"]',
        'expect_failures = [var.allowed_cidr_blocks]',
    ):
        if fragment not in allowed_cidr_blocks_test:
            errors.append(f"allowed CIDR Terraform test is missing contract: {fragment}")
    if 'variable "aws_region"' not in variables or "var.aws_region" not in variables:
        errors.append("variables.tf must define and validate aws_region")
    if 'variable "ami_id"' not in variables or "var.ami_id" not in variables:
        errors.append("variables.tf must define and validate ami_id")
    if 'variable "instance_type"' not in variables or "var.instance_type" not in variables:
        errors.append("variables.tf must define and validate instance_type")
    if 'can(regex("^[a-z0-9][a-z0-9-]*[.][a-z0-9]+$", var.instance_type))' not in variables:
        errors.append("instance_type must validate EC2 instance type syntax")
    if 'variable "resource_tags"' not in variables:
        errors.append("variables.tf must define common resource_tags")
    if "type        = map(string)" not in variables:
        errors.append("resource_tags must be a string map")
    if 'ManagedBy = "terraform"' not in variables or 'Project   = "terraform-basic-example"' not in variables:
        errors.append("resource_tags must include default ownership tags")
    for fragment in (
        "length(var.resource_tags) > 0",
        "length(trimspace(key)) > 0",
        "length(trimspace(value)) > 0",
        '!startswith(lower(key), "aws:")',
    ):
        if fragment not in variables:
            errors.append(f"resource_tags validation is missing contract: {fragment}")
    if 'variable "server_port"' in variables and "validation {" not in variables:
        errors.append("server_port must include Terraform variable validation")
    if "var.server_port == floor(var.server_port)" not in variables:
        errors.append("server_port must reject fractional port values")
    for fragment in (
        'mock_provider "aws" {}',
        'run "accept_default_server_port"',
        'run "reject_fractional_server_port"',
        "server_port = 8080.5",
        "expect_failures = [var.server_port]",
    ):
        if fragment not in server_port_test:
            errors.append(f"server port Terraform test is missing contract: {fragment}")
    for fragment in (
        'mock_provider "aws" {}',
        'run "accept_default_resource_tags"',
        'run "reject_empty_resource_tags"',
        'run "reject_blank_resource_tag_key"',
        'run "reject_blank_resource_tag_value"',
        'run "reject_reserved_resource_tag_key"',
        "resource_tags = {}",
        '"aws:owner" = "platform"',
    ):
        if fragment not in resource_tags_test:
            errors.append(f"resource tags Terraform test is missing contract: {fragment}")
    if resource_tags_test.count("expect_failures = [var.resource_tags]") != 4:
        errors.append("resource tags Terraform tests must expect all four validation failures")
    if "metadata_options" not in main or not re.search(r'http_tokens\s+=\s+"required"', main):
        errors.append("aws_instance.example must require IMDSv2 with http_tokens")
    if not re.search(r'http_put_response_hop_limit\s+=\s+1', main):
        errors.append("aws_instance.example must limit metadata response hops to 1")
    if "root_block_device" not in main or "encrypted = true" not in main:
        errors.append("aws_instance.example root block device must be encrypted")
    if not re.search(r'user_data_replace_on_change\s+=\s+true', main):
        errors.append("aws_instance.example must replace on user_data changes")

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("hygiene", "config"), required=True)
    args = parser.parse_args()

    errors = hygiene_checks() if args.mode == "hygiene" else config_checks()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"{args.mode} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
