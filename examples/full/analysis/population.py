import plotly.express as px
from boredcharts import FigureRouter
from plotly.graph_objects import Figure

figures = FigureRouter(prefix="/population")


@figures.chart("population")
async def example(report_name: str, country: str) -> Figure:
    df = px.data.gapminder().query(f"country=='{country}'")
    fig = px.bar(df, x="year", y="pop")
    fig.update_layout(
        plot_bgcolor="white",
        title=f"Population of {country}",
        xaxis=dict(
            title="",
            tickangle=-45,
        ),
        yaxis=dict(
            gridcolor="lightgrey",
            title="Population",
            minor=dict(ticks="inside"),
        ),
        legend=dict(title=""),
    )
    return fig


@figures.chart("usa_population")
async def fig_example_simple(report_name: str) -> Figure:
    return await example(report_name, "United States")
