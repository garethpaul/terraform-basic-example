.PHONY: build check lint test verify

override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3
TERRAFORM ?= terraform

lint:
	$(PYTHON) "$(ROOT)/scripts/check-terraform-source.py" --mode hygiene

test:
	$(PYTHON) "$(ROOT)/scripts/check-terraform-source.py" --mode config

build: lint
	@if command -v "$(TERRAFORM)" >/dev/null 2>&1; then \
		set -e; \
		cd "$(ROOT)"; \
		"$(TERRAFORM)" fmt -check -diff; \
		"$(TERRAFORM)" init -backend=false -lockfile=readonly; \
		"$(TERRAFORM)" validate -no-color; \
		"$(TERRAFORM)" test -no-color; \
	else \
		echo "terraform not found; static Terraform checks completed"; \
	fi

verify: lint test build

check: verify
