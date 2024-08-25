import matplotlib.figure as mplfig
import matplotlib.pyplot as plt
import numpy as np
from boredcharts import FigureRouter

figures = FigureRouter()


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
