.PHONY: dev
## Run locally
dev:
	UVICORN_RELOAD=true uv run bc-example

.PHONY: up
## Start docker compose
up:
	docker compose up --build

.PHONY: down
## Stop docker compose
down:
	docker compose down --remove-orphans
