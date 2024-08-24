import altair as alt
import plotly.express as px
from boredcharts import BCRouter

router = BCRouter()


@router.chart("medals")
async def medals() -> alt.Chart:
    df = px.data.medals_long()
    medals = {"gold": "#FFD700", "silver": "#C0C0C0", "bronze": "#CD7F32"}
    fig = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="nation:N",
            y="count:Q",
            color=alt.Color(
                "medal:N",
                scale=alt.Scale(
                    domain=list(medals.keys()), range=list(medals.values())
                ),
            ),
            xOffset=alt.XOffset(
                "medal:N",
                sort=alt.EncodingSortField(field="medal:N", order="ascending"),
            ),
            order=alt.Order("medal:N", sort="ascending"),
        )
        .interactive()
    )
    return fig
