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
│   ├── elasticity.py
│   ├── medals.py
│   ├── population.py
│   └── ...             <-- add more figures here
├── pages
│   ├── elasticity.md
│   ├── medals.md
│   ├── populations.md
│   └── ...             <-- add more reports here
├── app.py              <-- the main bored-charts app
├── README.md
└── pyproject.toml
```

It's also dockerized:

```bash
docker compose up --build
```
