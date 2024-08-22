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
