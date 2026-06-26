#!/usr/bin/env python3
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check-terraform-source.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("terraform_source_checker", CHECKER_PATH)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    return checker


def main():
    checker = load_checker()
    main_source = (ROOT / "main.tf").read_text(encoding="utf-8")
    variables_source = (ROOT / "variables.tf").read_text(encoding="utf-8")
    tests_source = (ROOT / "tests" / "resource_tags.tftest.hcl").read_text(encoding="utf-8")
    if checker.resource_tag_merge_errors(main_source):
        raise SystemExit("baseline resource tag merge contract failed")
    if checker.resource_tag_validation_errors(variables_source, tests_source):
        raise SystemExit("baseline resource tag validation contract failed")

    mutations = {
        "instance ownership tags": main_source.replace(
            '  tags = merge(var.resource_tags, {\n    Name = "terraform-example"\n  })',
            '  tags = {\n    Name = "terraform-example"\n  }',
            1,
        ),
        "security group ownership tags": main_source.replace(
            '  tags = merge(var.resource_tags, {\n    Name = "terraform-example-instance"\n  })',
            '  tags = {\n    Name = "terraform-example-instance"\n  }',
            1,
        ),
    }
    for name, mutated in mutations.items():
        if mutated == main_source:
            raise SystemExit(f"mutation setup failed for {name}")
        if not checker.resource_tag_merge_errors(mutated):
            raise SystemExit(f"resource tag contract accepted missing {name}")

    validation_mutations = {
        "canonical key whitespace": (
            variables_source.replace("        key == trimspace(key) &&\n", "", 1),
            tests_source,
        ),
        "canonical value whitespace": (
            variables_source.replace("        value == trimspace(value) &&\n", "", 1),
            tests_source,
        ),
        "canonical key whitespace native case": (
            variables_source,
            tests_source.replace(
                'run "reject_resource_tag_key_with_surrounding_whitespace"',
                'run "mutated_resource_tag_key_with_surrounding_whitespace"',
                1,
            ),
        ),
        "canonical value whitespace native case": (
            variables_source,
            tests_source.replace(
                'run "reject_resource_tag_value_with_surrounding_whitespace"',
                'run "mutated_resource_tag_value_with_surrounding_whitespace"',
                1,
            ),
        ),
    }
    for name, (mutated_variables, mutated_tests) in validation_mutations.items():
        if mutated_variables == variables_source and mutated_tests == tests_source:
            raise SystemExit(f"mutation setup failed for {name}")
        if not checker.resource_tag_validation_errors(mutated_variables, mutated_tests):
            raise SystemExit(f"resource tag contract accepted missing {name}")

    mutation_count = len(mutations) + len(validation_mutations)
    print(f"resource tag contract passed ({mutation_count} mutations rejected)")


if __name__ == "__main__":
    main()
