#!/usr/bin/env python3
import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check-terraform-source.py"
EXPECTED_ERROR = "CI workflow must match the reviewed credential-free Terraform validation contract"


def load_checker():
    spec = importlib.util.spec_from_file_location("terraform_source_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load Terraform source checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise AssertionError(f"workflow fixture did not contain exactly one {old!r}")
    return source.replace(old, new, 1)


def main():
    checker = load_checker()
    workflow = checker.CI_WORKFLOW.read_text(encoding="utf-8")
    if workflow != checker.EXPECTED_WORKFLOW:
        raise AssertionError("checked-in workflow does not match the source checker contract")

    mutations = (
        ("write permissions", "contents: read", "contents: write"),
        ("credential persistence", "persist-credentials: false", "persist-credentials: true"),
        ("checkout pin", "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10", "actions/checkout@main"),
        ("Python action pin", "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405", "actions/setup-python@v6"),
        ("Terraform action pin", "hashicorp/setup-terraform@dfe3c3f87815947d99a8997f908cb6525fc44e9e", "hashicorp/setup-terraform@v4"),
        ("runner", "runs-on: ubuntu-24.04", "runs-on: ubuntu-latest"),
        ("timeout", "timeout-minutes: 10", "timeout-minutes: 30"),
        ("concurrency cancellation", "cancel-in-progress: true", "cancel-in-progress: false"),
        ("concurrency key", "group: check-${{ github.workflow }}-${{ github.ref }}", "group: check-${{ github.workflow }}"),
        ("Python version", 'python-version: "3.12"', 'python-version: "3.11"'),
        ("Terraform version", 'terraform_version: "1.15.6"', 'terraform_version: "1.14.0"'),
        ("Terraform wrapper", "terraform_wrapper: false", "terraform_wrapper: true"),
        ("unqualified Make", "run: /usr/bin/make check", "run: make check"),
        ("shell wrapper", "run: /usr/bin/make check", "run: /bin/sh -c '/usr/bin/make check'"),
        ("pull request target", "  pull_request:\n", "  pull_request_target:\n"),
        ("secret environment", "    timeout-minutes: 10\n", "    timeout-minutes: 10\n    env:\n      TOKEN: ${{ secrets.TOKEN }}\n"),
        ("extra checkout credentials", "          persist-credentials: false\n", "          persist-credentials: false\n          token: ${{ github.token }}\n"),
    )

    original_path = checker.CI_WORKFLOW
    with tempfile.TemporaryDirectory(prefix="terraform-workflow-contract-") as temp_dir:
        for name, old, new in mutations:
            mutated_path = Path(temp_dir) / "check.yml"
            mutated_path.write_text(replace_once(workflow, old, new), encoding="utf-8")
            checker.CI_WORKFLOW = mutated_path
            errors = checker.hygiene_checks()
            if EXPECTED_ERROR not in errors:
                raise AssertionError(f"workflow mutation was not rejected: {name}")
    checker.CI_WORKFLOW = original_path
    print(f"workflow contract passed ({len(mutations)} mutations rejected)")


if __name__ == "__main__":
    main()
