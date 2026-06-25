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
    if checker.resource_tag_merge_errors(main_source):
        raise SystemExit("baseline resource tag merge contract failed")

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

    print(f"resource tag merge contract passed ({len(mutations)} mutations rejected)")


if __name__ == "__main__":
    main()
