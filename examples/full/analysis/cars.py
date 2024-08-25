import altair as alt
from boredcharts import FigureRouter
from vega_datasets import data

figures = FigureRouter()


@figures.chart("cars.scatter-correlation")
async def cars() -> alt.RepeatChart:
    """
    source: https://altair-viz.github.io/gallery/scatter_matrix.html
    """
    source = data.cars()

    fig = (
        alt.Chart(source)
        .mark_circle()
        .encode(
            alt.X(alt.repeat("column"), type="quantitative"),
            alt.Y(alt.repeat("row"), type="quantitative"),
            color="Origin:N",
        )
        .properties(width=150, height=150)
        .repeat(
            row=["Horsepower", "Acceleration", "Miles_per_Gallon"],
            column=["Miles_per_Gallon", "Acceleration", "Horsepower"],
        )
        .properties(title="Correlation of car specs by where they were made")
        .interactive()
    )
    return fig
