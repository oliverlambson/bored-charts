# bored-charts

Build easy, minimal, PDF-able data reports with markdown and python.

## Roadmap

- [ ] custom figures for individual reports using path parameters
- [ ] installable as a framework
- [ ] example with database
- [ ] authentication
- [ ] pdf exports
- [ ] cli?

## Setup

You'll need [rye](https://rye.astral.sh/guide/installation/).
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

## References

Inspired by [evidence.dev](https://github.com/evidence-dev/evidence),
[observable framework](https://github.com/observablehq/framework), and
[rill](https://github.com/rilldata/rill), but:
(1) I wanted to use python for data analysis and charting,
(2) I didn't want a static site, and
(3) I didn't want to pay for deployment.
