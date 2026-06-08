#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def tracked_files():
    output = subprocess.check_output(["git", "ls-files"], cwd=str(ROOT), text=True)
    return output.splitlines()


def hygiene_checks():
    errors = []
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
    if 'cidr_blocks = ["0.0.0.0/0"]' in main:
        errors.append("security group ingress must use configurable CIDR blocks")
    if "cidr_blocks = var.allowed_cidr_blocks" not in main:
        errors.append("security group ingress must reference var.allowed_cidr_blocks")
    if 'variable "allowed_cidr_blocks"' not in variables:
        errors.append("variables.tf must define allowed_cidr_blocks")
    if 'variable "server_port"' in variables and "validation {" not in variables:
        errors.append("server_port must include Terraform variable validation")

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
