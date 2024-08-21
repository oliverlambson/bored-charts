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
	rye sync
	npm i

.PHONY: test
## Run test
test:
	rye run mypy .
	rye run pytest

.PHONY: lint
## Run linting
lint:
	rye run ruff check .
	rye run ruff format . --check
	rye run mdformat README.md --check
	npx prettier . --check

.PHONY: fmt
## Run linting
fmt:
	rye run ruff check . --fix
	rye run ruff format .
	rye run mdformat README.md
	npx prettier . --write

.PHONY: dev
## Run locally
dev:
	UVICORN_RELOAD=true rye run bc-example

.PHONY: d.up
## Start docker compose
d.up:
	docker compose up --build

.PHONY: d.down
## Stop docker compose
d.down:
	docker compose down --remove-orphans
