.DEFAULT_GOAL := help

YELLOW := \033[0;33m
RESET := \033[0m

.PHONY: help
## Prints this help
help:
	@echo "\nUsage: make ${YELLOW}[arg=value] <target>${RESET}\n\nThe following targets are available:\n";
	@awk -v skip=1 \
		'/^##/ { sub(/^[#[:blank:]]*/, "", $$0); doc_h=$$0; doc=""; skip=0; next } \
		 skip  { next } \
		 /^#/  { doc=doc "\n" substr($$0, 2); next } \
		 /:/   { sub(/:.*/, "", $$0); printf "\033[34m%-30s\033[0m\033[1m%s\033[0m %s\n", $$0, doc_h, doc; skip=1 }' \
		$(MAKEFILE_LIST)

.PHONY: env
## (Re-)create virtual environment
env:
	rm -rf .venv
	rm -rf node_modules
	uv sync
	npm i

.PHONY: test
## Run test
test:
	uv run mypy .
	uv run pytest

.PHONY: lint
## Run linting
lint:
	uv run ruff check .
	uv run ruff format . --check
	uv run mdformat README.md --check
	npx prettier . --check

.PHONY: fmt
## Run linting
fmt:
	uv run ruff check . --fix
	uv run ruff format .
	uv run mdformat README.md
	npx prettier . --write

.PHONY: clean
## Remove all hidden generated/cache files
clean:
	find . -type d \( -name "__pycache__" -o -name ".ruff_cache" -o -name ".mypy_cache" -o -name ".pytest_cache" \) -exec rm -rf {} +
