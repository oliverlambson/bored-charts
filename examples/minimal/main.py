from pathlib import Path

import plotly.express as px
from boredcharts import BCRouter, boredcharts
from boredcharts.jinja import to_html
from fastapi.responses import HTMLResponse

pages = Path(__file__).parent.absolute() / "pages"
figure_router = BCRouter()


@figure_router.chart("usa_population")
async def usa_population() -> HTMLResponse:
    df = px.data.gapminder().query("country=='United States'")
    fig = px.bar(df, x="year", y="pop")
    return HTMLResponse(to_html(fig))


app = boredcharts(
    pages=pages,
    figure_router=figure_router,
)
