# bored-charts full example app

Run it:

```bash
uv run bc-example
```

Project structure:

```
.
├── analysis
│   ├── __init__.py
│   ├── cars.py
│   ├── elasticity.py
│   ├── medals.py
│   ├── population.py
│   └── ...                   <-- add more figures here
├── pages
│   ├── more                  - note you can create nested paths:
│   │   └── test.md             <- this will be at /more/test
│   ├── populations.md          <- this will be at /populations
│   ├── price-elasticity.md
│   ├── vega-lite-is-cool.md
│   └── ...                   <-- add more reports here
├── app.py                    - the main bored-charts app
├── pyproject.toml
└── README.md
```

It's also dockerized:

```bash
docker compose up --build
```
