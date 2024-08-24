FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN useradd --uid 1001 --user-group --home-dir=/home/bored-charts --create-home --shell=/bin/false bored-charts
USER bored-charts

COPY --chown=bored-charts pyproject.toml /app/pyproject.toml
RUN chown bored-charts:bored-charts /app

WORKDIR /app
RUN uv sync --no-install-project --no-install-workspace --no-dev --compile-bytecode

COPY --chown=bored-charts . /app
WORKDIR /app

RUN uv sync --no-dev --compile-bytecode

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
EXPOSE 4000
CMD ["bc-example"]
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:4000/healthz"]
