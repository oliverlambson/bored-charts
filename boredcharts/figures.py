import plotly.express as px
from plotly.graph_objects import Figure


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
