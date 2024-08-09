FROM python:3.12-slim AS base

RUN apt-get update && \
  apt-get install -y curl && \
  rm -rf /var/lib/apt/lists/* && \
  useradd --uid 1001 --user-group --home-dir=/home/bored-charts --create-home --shell=/bin/false bored-charts

# ------------------------------------------------------------------------------
FROM base AS app

WORKDIR /app
RUN chown bored-charts:bored-charts /app

COPY --chown=bored-charts requirements.lock pyproject.toml ./
RUN mkdir -p src/boredcharts/ && \
  touch README.md src/boredcharts/__init__.py && \
  pip install -r requirements.lock

COPY --chown=bored-charts ./ /app/

WORKDIR /app

ENV PYTHONUNBUFFERED=1
USER bored-charts
EXPOSE 4000
CMD ["boredcharts"]
HEALTHCHECK CMD ["curl", "--fail", "http://localhost:4000/healthz"]
