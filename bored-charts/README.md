# bored-charts

Build easy, minimal, PDF-able data reports with markdown and python.

## Minimal example

Install bored-charts and uvicorn:

```bash
pip install bored-charts uvicorn
```

Create your app:

```python
# app.py
from pathlib import Path

import plotly.express as px
from boredcharts import boredcharts
from boredcharts.jinja import to_html
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

pages = Path(__file__).parent.absolute() / "pages"
figure_router = APIRouter()


@figure_router.get("/report/{report_name}/figure/usa_population", name="usa_population")
async def usa_population(report_name: str) -> HTMLResponse:
    df = px.data.gapminder().query("country=='United States'")
    fig = px.bar(df, x="year", y="pop")
    return HTMLResponse(to_html(fig))


app = boredcharts(
    pages=pages,
    figure_router=figure_router,
)
```

Write a markdown report:

```md
<!-- pages/populations.md -->

## Populations

USA's population has been growing linearly for the last 70 years:

{{ figure("usa_population") }}
```

Run your app:

```bash
uvicorn app:app --reload
```

A more full project structure might look like this:

```
my-reports
├── myreports
│   ├── pages <-- put your markdown reports here
│   │   └── example.md
│   ├── **init**.py
│   ├── app.py <-- spin up the app here
│   └── figures.py <-- define your figures here
├── README.md
└── pyproject.toml
```
