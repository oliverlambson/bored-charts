from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
from boredcharts import FigureRouter, boredcharts

figures = FigureRouter()


@figures.chart("population")
async def population(country: str) -> go.Figure:
    df = px.data.gapminder().query(f"country=='{country}'")
    fig = px.bar(df, x="year", y="pop")
    return fig


app = boredcharts(pages=Path(__file__).parent, figures=figures)
