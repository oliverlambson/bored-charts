# bored-charts

Build easy, minimal, PDF-able data reports with markdown and python.

## Roadmap

- [x] custom figures for individual reports using path parameters
- [x] dynamic figure sizing using flexbox
- [x] installable as a framework
- [x] example project
- [x] separate pyproject.toml for lib and example
- [x] publish to pypi
- [x] less boilerplate to register figure endpoints
  - [x] @bored_router.chart decorator
  - [x] allow decoration of functions that return figures directly
- [x] make report_name path parameter optional
- [x] altair figures as html
- [x] matplotlib figures as png (drop mpld3)
- [x] allow nested pages for grouping reports
- [ ] matplotlib figures as svg?
- [ ] make plotting libraries optional
- [ ] pdf exports with selenium in headless mode
- [ ] cli? (`boredcharts init`, `boredcharts export [report]`, `boredcharts dev`, `boredcharts serve`)
- [ ] deploy to [bored-charts-example.oliverlambson.com](https://bored-charts-example.oliverlambson.com)
- [ ] dashboard layout with tighter grid layout
- [ ] example with database
- [ ] example with authentication

## Usage

See [bored-charts/README.md](./bored-charts/README.md) (you're currently reading the development README).

## Development

You'll need [uv](https://docs.astral.sh/uv/getting-started/installation/).
(and [node](https://nodejs.org/en/learn/getting-started/how-to-install-nodejs)
for linting/formatting, sorry)

```bash
make env  # you need uv & node for this
make test
make lint
make fmt
```

I recommend running the full example project to see how everything fits together:

```bash
cd examples/full
make dev
```

## Built with

- [fastapi](https://fastapi.tiangolo.com/)
- [htmx](https://htmx.org/)
- [jinja](https://jinja.palletsprojects.com/en/3.1.x/)
- [tailwindcss](https://tailwindcss.com/)

## Alternatives

Inspired by [evidence.dev](https://github.com/evidence-dev/evidence),
[observable framework](https://github.com/observablehq/framework), and
[rill](https://github.com/rilldata/rill), but:
(1) I wanted to use python for data analysis and charting,
(2) I didn't want a static site, and
(3) I didn't want to pay for deployment.

You could also achieve something similar with pandoc and nbconvert,
see [examples/\_alternatives](https://github.com/oliverlambson/bored-charts/tree/main/examples/_alternatives) for more.
