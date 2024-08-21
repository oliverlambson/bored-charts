import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, StrictUndefined
from plotly.offline import get_plotlyjs

from boredcharts.figures import router as figure_router
from boredcharts.jinja import figure, md_to_html, row

module_root = Path(__file__).parent.absolute()
static_root = module_root / "static"
templates_root = module_root / "templates"
pages_root = module_root / "pages"

Path(static_root / "plotlyjs.min.js").write_text(get_plotlyjs())

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=static_root),
    "static",
)
templates = Jinja2Templates(
    directory=[pages_root, templates_root],  # user can overwrite templates with pages
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
        pages_root.glob("*.md"),
        reverse=True,
    )
]
templates.env.filters["markdown"] = md_to_html
templates.env.globals["figure"] = figure
templates.env.globals["row"] = row


@app.get("/")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


# TODO: pass pages path into framework, auto generate this route
@app.get("/report/{report_name}", name="report")
async def report(report_name: str, request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "report": report_name,
        },
    )


app.mount("/", figure_router)


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
