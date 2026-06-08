.PHONY: build check lint test verify

PYTHON ?= python3
TERRAFORM ?= terraform

lint:
	$(PYTHON) scripts/check-terraform-source.py --mode hygiene

test:
	$(PYTHON) scripts/check-terraform-source.py --mode config

build: lint
	@if command -v "$(TERRAFORM)" >/dev/null 2>&1; then \
		"$(TERRAFORM)" fmt -check; \
		"$(TERRAFORM)" init -backend=false; \
		"$(TERRAFORM)" validate; \
	else \
		echo "terraform not found; static Terraform checks completed"; \
	fi

verify: lint test build

check: verify
