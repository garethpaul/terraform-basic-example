#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs" / "plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-terraform-basic-example-baseline.md"


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def tracked_files():
    output = subprocess.check_output(["git", "ls-files"], cwd=str(ROOT), text=True)
    return output.splitlines()


def hygiene_checks():
    errors = []
    if not CANONICAL_PLAN.exists():
        errors.append("docs/plans/2026-06-08-terraform-basic-example-baseline.md is missing")

    plans = sorted(DOCS_PLANS.glob("*.md")) if DOCS_PLANS.exists() else []
    if not plans:
        errors.append("docs/plans must contain at least one completed plan")
    for plan_path in plans:
        plan = plan_path.read_text(encoding="utf-8")
        if "Status: Completed" not in plan or "make check" not in plan:
            errors.append(f"{plan_path.relative_to(ROOT)} must record completed status and make check verification")

    gitignore = read_text(".gitignore") if (ROOT / ".gitignore").exists() else ""
    for pattern in (".terraform/", "*.tfstate", "*.tfstate.*", "*.tfvars", "crash.log"):
        if pattern not in gitignore:
            errors.append(f".gitignore must include Terraform pattern: {pattern}")

    for path in tracked_files():
        if path.endswith(".tfstate") or ".tfstate." in path or path.endswith(".tfvars"):
            errors.append(f"state or local variable file must not be tracked: {path}")

    return errors


def config_checks():
    errors = []
    main = read_text("main.tf")
    variables = read_text("variables.tf")

    if "required_providers" not in main or 'source  = "hashicorp/aws"' not in main:
        errors.append("main.tf must declare the hashicorp/aws provider source")
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
    if 'variable "allowed_cidr_blocks"' not in variables:
        errors.append("variables.tf must define allowed_cidr_blocks")
    if "var.allowed_cidr_blocks" not in variables or "cidrhost(cidr, 0)" not in variables:
        errors.append("allowed_cidr_blocks must validate CIDR values")
    if 'variable "aws_region"' not in variables or "var.aws_region" not in variables:
        errors.append("variables.tf must define and validate aws_region")
    if 'variable "ami_id"' not in variables or "var.ami_id" not in variables:
        errors.append("variables.tf must define and validate ami_id")
    if 'variable "instance_type"' not in variables or "var.instance_type" not in variables:
        errors.append("variables.tf must define and validate instance_type")
    if 'variable "server_port"' in variables and "validation {" not in variables:
        errors.append("server_port must include Terraform variable validation")
    if "metadata_options" not in main or 'http_tokens = "required"' not in main:
        errors.append("aws_instance.example must require IMDSv2 with http_tokens")
    if "root_block_device" not in main or "encrypted = true" not in main:
        errors.append("aws_instance.example root block device must be encrypted")

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
