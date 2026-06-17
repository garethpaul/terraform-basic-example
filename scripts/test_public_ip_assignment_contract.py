#!/usr/bin/env python3
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENT = "associate_public_ip_address = length(var.allowed_cidr_blocks) > 0"


def contract_errors(main, allowed_cidr_test):
    errors = []
    if len(re.findall(r"^\s*associate_public_ip_address\s*=", main, re.MULTILINE)) != 1:
        errors.append("the instance must contain exactly one public IPv4 assignment")
    if ASSIGNMENT not in main:
        errors.append("public IPv4 assignment must derive from non-empty allowed CIDRs")
    for expected in (
        "aws_instance.example.associate_public_ip_address == false",
        "aws_instance.example.associate_public_ip_address == true",
    ):
        if expected not in allowed_cidr_test:
            errors.append(f"mocked Terraform tests are missing: {expected}")
    return errors


def main():
    main_source = (ROOT / "main.tf").read_text(encoding="utf-8")
    test_source = (ROOT / "tests" / "allowed_cidr_blocks.tftest.hcl").read_text(
        encoding="utf-8"
    )
    baseline_errors = contract_errors(main_source, test_source)
    if baseline_errors:
        raise SystemExit("baseline public IPv4 contract failed: " + "; ".join(baseline_errors))

    mutations = {
        "omitted assignment": "",
        "unconditional assignment": "associate_public_ip_address = true",
        "unconditional private assignment": "associate_public_ip_address = false",
        "inverted condition": (
            "associate_public_ip_address = length(var.allowed_cidr_blocks) == 0"
        ),
        "input-independent condition": "associate_public_ip_address = var.server_port > 0",
    }
    for name, replacement in mutations.items():
        mutated = main_source.replace(ASSIGNMENT, replacement, 1)
        if mutated == main_source:
            raise SystemExit(f"mutation setup failed for {name}")
        if not contract_errors(mutated, test_source):
            raise SystemExit(f"public IPv4 contract accepted {name}")

    print(f"public IPv4 assignment contract passed ({len(mutations)} mutations rejected)")


if __name__ == "__main__":
    main()
