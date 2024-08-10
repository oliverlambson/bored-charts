import os
from pathlib import Path

import markdown
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, StrictUndefined
from markupsafe import Markup
from plotly.graph_objects import Figure

from .figures import example


def to_html(fig: Figure) -> Markup:
    if not isinstance(fig, Figure):
        raise ValueError(f"Input must be a Plotly Figure, got {type(fig)}")
    return Markup(
        fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            default_height="100%",
            default_width="100%",
            config={
                "displaylogo": False,
                "responsive": True,
                "displayModeBar": False,
            },
        )
    )


def md_to_html(md: str) -> Markup:
    return Markup(markdown.markdown(md))


module_root = Path(__file__).parent.absolute()
app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=module_root / "static"),
    "static",
)
templates = Jinja2Templates(
    directory=module_root / "templates",
    env=Environment(
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    ),
)
templates.env.globals["title"] = "bored charts"
templates.env.globals["reports"] = [
    {"name": f.stem}
    for f in sorted(
        (module_root / "templates" / "pages").glob("*.md"),
        reverse=True,
    )
]
templates.env.filters["markdown"] = md_to_html
templates.env.filters["html"] = to_html


@app.get("/")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get("/report/{report_name}", name="report")
async def report(report_name: str, request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "report": report_name,
        },
    )


@app.get("/report/{report_name}/figure/example_simple_usa", name="example_simple_usa")
async def fig_example_simple(report_name: str) -> HTMLResponse:
    return HTMLResponse(to_html(await example(report_name, "United States")))


@app.get("/report/{report_name}/figure/example_params", name="example_params")
async def fig_example(report_name: str, country: str) -> HTMLResponse:
    return HTMLResponse(to_html(await example(report_name, country)))


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


def entrypoint() -> None:
    import uvicorn

    uvicorn.run(
        f"{__name__}:app",
        host=os.getenv("UVICORN_HOST", "127.0.0.1"),
        port=4000,
        reload=os.getenv("UVICORN_RELOAD", "false").upper() == "TRUE",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    entrypoint()
