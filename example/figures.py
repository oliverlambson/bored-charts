import matplotlib.figure as mplfig
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from plotly.graph_objects import Figure

from boredcharts.jinja import to_html

router = APIRouter()


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


# TODO: pass functions into framework, auto generate these routes
@router.get(
    "/report/{report_name}/figure/example_simple_usa", name="example_simple_usa"
)
async def fig_example_simple(report_name: str) -> HTMLResponse:
    return HTMLResponse(to_html(await example(report_name, "United States")))


@router.get("/report/{report_name}/figure/example_params", name="example_params")
async def fig_example(report_name: str, country: str) -> HTMLResponse:
    return HTMLResponse(to_html(await example(report_name, country)))


async def elasticity_vs_profit(
    report_name: str, margin: float | None = None
) -> mplfig.Figure:
    n = 1000
    price_range = (-1, 1 + 1 / n)
    qty_range = (-1, 5 + 1 / n)
    price_values = np.linspace(*price_range, n)
    qty_values = np.linspace(*qty_range, n)
    margin_values = np.arange(0.1, 1.00, 0.1)

    P, Q = np.meshgrid(price_values, qty_values)

    RHS = -P * (1 / Q + 1)

    fig, ax = plt.subplots(figsize=(10, 6))
    # fig, ax = plt.subplots()

    for i, margin in enumerate(margin_values):
        mask = np.where(Q >= 0, margin > RHS, margin < RHS)  # pyright: ignore[reportOptionalOperand]
        ax.contourf(P, Q, mask, levels=[0.5, 1], alpha=0.15)

    contours = []
    for margin in margin_values:
        mask = np.where(Q >= 0, margin > RHS, margin < RHS)  # pyright: ignore[reportOptionalOperand]
        contour = ax.contour(P, Q, mask, levels=[0], colors="black", linewidths=0.5)
        contours.append(contour)

    for i, contour in enumerate(contours):
        suffix = " margin" if i == 0 else ""
        paths = contour.collections[0].get_paths()
        label_positions = [
            path.vertices[int(0.1 * len(path.vertices))]  # type: ignore[index,operator,arg-type]
            for path in paths
        ]
        ax.clabel(
            contour,
            inline=True,
            fontsize=8,
            fmt={0: f"{margin_values[i]:.0%}{suffix}"},
            manual=label_positions,
            use_clabeltext=True,
        )

    ax.set_xlabel("Change in Price")
    ax.set_ylabel("Change in Quantity")
    ax.set_xticks(
        np.arange(*price_range, 0.1), [f"{x:.0%}" for x in np.arange(*price_range, 0.1)]
    )
    ax.set_yticks(
        np.arange(*qty_range, 1), [f"{y:.0%}" for y in np.arange(*qty_range, 1)]
    )
    ax.set_title("Profitable regions given change in price & qty for set margin")
    ax.grid(True)

    return fig


# TODO: pass functions into framework, auto generate these routes
@router.get(
    "/report/{report_name}/figure/elasticity_vs_profit", name="elasticity_vs_profit"
)
async def fig_elasticity_vs_profit(
    report_name: str, margin: float | None = None
) -> HTMLResponse:
    return HTMLResponse(to_html(await elasticity_vs_profit(report_name, margin)))
