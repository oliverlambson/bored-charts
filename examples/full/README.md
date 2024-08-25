# bored-charts full example app

Run it:

```bash
uv run bc-example
```

Project structure:

```
.
├── app
│   ├── __init__.py
│   ├── elasticity.py    # analysis on price elasticity
│   ├── main.py          # the main bored-charts app
│   ├── medals.py        # analysis on olympic medals
│   ├── population.py    # analysis on world population growth
│   └── ...             <-- add more figures here
├── pages
│   ├── medals.md
│   ├── populations.md
│   └── ...             <-- add more reports here
├── README.md
└── pyproject.toml
```

It's also dockerized:

```bash
docker compose up --build
```
