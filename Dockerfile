FROM python:3.12-slim AS base

RUN apt-get update && \
  apt-get install -y --no-install-recommends curl ca-certificates && \
  rm -rf /var/lib/apt/lists/* && \
  useradd --uid 1001 --user-group --home-dir=/home/bored-charts --create-home --shell=/bin/false bored-charts
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.cargo/bin/:$PATH"

# ------------------------------------------------------------------------------
FROM base AS app

WORKDIR /app
RUN chown bored-charts:bored-charts /app

COPY --chown=bored-charts uv.lock pyproject.toml ./
COPY --chown=bored-charts bored-charts/pyproject.toml ./bored-charts/pyproject.toml
COPY --chown=bored-charts bored-charts/boredcharts/__init__.py ./bored-charts/boredcharts/__init__.py
COPY --chown=bored-charts example/pyproject.toml ./example/pyproject.toml
COPY --chown=bored-charts example/bcexample/__init__.py ./example/bcexample/__init__.py
RUN touch README.md bored-charts/README.md example/README.md && \
  uv sync --locked --no-dev

COPY --chown=bored-charts ./ /app/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
USER bored-charts
EXPOSE 4000
CMD ["bc-example"]
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:4000/healthz"]
