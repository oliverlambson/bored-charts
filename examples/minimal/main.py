from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
from boredcharts import BCRouter, boredcharts

pages = Path(__file__).parent.absolute() / "pages"
figure_router = BCRouter()


@figure_router.chart("population")
async def population(country: str) -> go.Figure:
    df = px.data.gapminder().query(f"country=='{country}'")
    fig = px.bar(df, x="year", y="pop")
    return fig


app = boredcharts(
    pages=pages,
    figure_router=figure_router,
)
