# bored-charts

Build easy, minimal, PDF-able data reports with markdown and python.

## Roadmap

- [x] custom figures for individual reports using path parameters
- [x] dynamic figure sizing using flexbox
- [x] installable as a framework
- [x] example project
- [x] separate pyproject.toml for lib and example
- [ ] publish to pypi
- [ ] deploy to [bored-charts-example.oliverlambson.com](https://bored-charts-example.oliverlambson.com)
- [ ] dashboard layout with grid layout
- [ ] example with database
- [ ] authentication
- [ ] pdf exports
- [ ] cli?

## Setup

You'll need [uv](https://docs.astral.sh/uv/getting-started/installation/).
(and [node](https://nodejs.org/en/learn/getting-started/how-to-install-nodejs)
for linting/formatting, sorry)

```bash
make env  # sets up python virtual environment
make dev  # runs bored-charts at http://localhost:4000
```

## Development

```bash
make dev  # runs bored-charts at http://localhost:4000
make test # runs tests
make lint # runs linting
make fmt  # runs formatting
```

## Built with

- [fastapi](https://fastapi.tiangolo.com/)
- [htmx](https://htmx.org/)
- [jinja](https://jinja.palletsprojects.com/en/3.1.x/)
- [tailwindcss](https://tailwindcss.com/)
- [plotly](https://plotly.com/python/)

## Alternatives

Inspired by [evidence.dev](https://github.com/evidence-dev/evidence),
[observable framework](https://github.com/observablehq/framework), and
[rill](https://github.com/rilldata/rill), but:
(1) I wanted to use python for data analysis and charting,
(2) I didn't want a static site, and
(3) I didn't want to pay for deployment.
