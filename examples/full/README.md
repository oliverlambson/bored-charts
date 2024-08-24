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
│   ├── figures.py      <-- add your figures here
│   └── main.py
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
