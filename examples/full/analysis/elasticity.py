import matplotlib.figure as mplfig
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from boredcharts import FigureRouter

figures = FigureRouter()


@figures.chart("price_vs_quantity")
async def price_vs_quantity(margin: float) -> mplfig.Figure:
    """plot the profitable frontier of price vs quantity for a given margin"""

    # experiment results
    results = pd.DataFrame(
        [
            (+0.05, -0.100),
            (-0.03, +0.075),
            (-0.07, +0.175),
            (-0.10, +0.200),
        ],
        columns=["price", "qty"],  # pyright: ignore[reportArgumentType]
    )

    # simulation
    n = 1000
    price_range = (-0.14, 0.14 + 1 / n)
    qty_range = (-0.4, 0.8 + 1 / n)
    price_values = np.linspace(*price_range, n)
    qty_values = np.linspace(*qty_range, n)

    P, Q = np.meshgrid(price_values, qty_values)

    RHS = -P * (1 / Q + 1)

    fig, ax = plt.subplots(figsize=(10, 6))
    mask = np.where(Q >= 0, margin > RHS, margin < RHS)  # pyright: ignore[reportOptionalOperand]
    ax.contourf(P, Q, mask, levels=[0.5, 1], alpha=0.5)
    ax.contour(P, Q, mask, levels=[0], colors="black", linewidths=0.5)
    ax.plot(results.price, results.qty, "rx", markersize=10, markeredgewidth=2)

    ax.set_title(f"Profitable region given change in price & qty for {margin=:.0%}")
    ax.set_xlabel("Change in Price")
    ax.set_ylabel("Change in Quantity")
    xticks = np.arange(*price_range, 0.02)
    yticks = np.arange(*qty_range, 0.1)
    ax.set_xticks(xticks, [f"{x:.0%}" for x in xticks])
    ax.set_yticks(yticks, [f"{y:.0%}" for y in yticks])
    ax.grid(True)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)

    return fig


@figures.chart("profit_at_price_drop")
async def profit_at_price_drop(drop: float) -> mplfig.Figure:
    """sensitivity of profit to elasticity for a given price drop"""

    base_profit = 760_000
    n = 1000
    elasticity_deviation_range = (-0.10, 0.10 + 1 / n)
    elasticity_deviation = np.linspace(*elasticity_deviation_range, n)
    # pretend we worked out this function and it's true
    profit_values = (
        elasticity_deviation * (10 * drop) * base_profit + base_profit * 1.05
    )

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(elasticity_deviation, profit_values, linestyle="-")
    ax.axhline(base_profit, color="black", linestyle="--")
    ax.text(0.04, base_profit, "Current profit", va="bottom")
    ax.fill_between(
        elasticity_deviation_range,
        700_000,
        base_profit,
        color="gray",
        alpha=0.5,
    )

    ax.set_title(f"Profit sensitivity to elasticity for price {drop=:.0%}")
    ax.set_xlabel("Elasticity deviation from expected (%)")
    ax.set_ylabel("Profit ($)")
    xticks = np.arange(*elasticity_deviation_range, 0.02)
    ax.set_xticks(xticks, [f"{x:.0%}" for x in xticks])
    ax.set_xlim(*elasticity_deviation_range)
    ax.set_ylim(700000, 850000)
    ax.yaxis.set_major_formatter("${x:,.0f}")
    ax.axvline(0, color="black", linewidth=0.5)
    ax.grid(True)
    fig.tight_layout()

    return fig


@figures.chart("elasticity_vs_profit")
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

    ax.set_title("Profitable regions given change in price & qty for various margins")
    ax.set_xlabel("Change in Price")
    ax.set_ylabel("Change in Quantity")
    xticks = np.arange(*price_range, 0.1)
    yticks = np.arange(*qty_range, 1)
    ax.set_xticks(xticks, [f"{x:.0%}" for x in xticks])
    ax.set_yticks(yticks, [f"{y:.0%}" for y in yticks])
    ax.hlines(0, *price_range, color="black", linewidth=0.5)
    ax.vlines(0, *qty_range, color="black", linewidth=0.5)
    ax.grid(True)

    return fig
