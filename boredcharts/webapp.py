import os
import string
import uuid
from pathlib import Path
from textwrap import dedent

import mpld3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, StrictUndefined
from plotly.offline import get_plotlyjs

from boredcharts.figures import elasticity_vs_profit, example
from boredcharts.jinja import figure, md_to_html, row, to_html

module_root = Path(__file__).parent.absolute()
Path(module_root / "static" / "plotlyjs.min.js").write_text(get_plotlyjs())
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


# ------------------------------------------------------------------------------
# TODO: the stuff below should be abstracted away from the framework user
# ------------------------------------------------------------------------------


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


# TODO: pass functions into framework, auto generate these routes
@app.get("/report/{report_name}/figure/example_simple_usa", name="example_simple_usa")
async def fig_example_simple(report_name: str) -> HTMLResponse:
    return HTMLResponse(to_html(await example(report_name, "United States")))


@app.get("/report/{report_name}/figure/example_params", name="example_params")
async def fig_example(report_name: str, country: str) -> HTMLResponse:
    return HTMLResponse(to_html(await example(report_name, country)))


@app.get(
    "/report/{report_name}/figure/elasticity_vs_profit", name="elasticity_vs_profit"
)
async def fig_elasticity_vs_profit(
    report_name: str, margin: float | None = None
) -> HTMLResponse:
    # TODO: return base64 encoded PNG instead of using mpld3
    figid = uuid.uuid4()
    script = dedent(
        string.Template(
            """
                <script>
                async function resizeMpld3(event, figid) {
                    var targetDiv = event.detail.elt.querySelector(`#${figid}`);
                    if (targetDiv) {
                        var svgElements = targetDiv.querySelectorAll('.mpld3-figure');
                        svgElements.forEach(function(svgElement) {
                            var width = svgElement.getAttribute('width');
                            var height = svgElement.getAttribute('height');
                            svgElement.setAttribute('viewBox', `0 0 ${width} ${height}`);
                            svgElement.setAttribute('width', '100%');
                            svgElement.removeAttribute('height');
                        });
                    }
                }
                document.addEventListener("htmx:afterSettle", (event) => { resizeMpld3(event, "${figid}") });
                </script>
            """
        ).safe_substitute(figid=figid)
    ).strip()
    return HTMLResponse(
        mpld3.fig_to_html(
            await elasticity_vs_profit(report_name, margin),
            no_extras=True,
            figid=str(figid),
        )
        + script
    )


# ------------------------------------------------------------------------------
# endTODO
# ------------------------------------------------------------------------------


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
