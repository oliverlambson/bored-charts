import base64
import logging
import uuid
from io import BytesIO
from textwrap import dedent, indent
from typing import Any, TypeAlias, cast

import altair as alt
import markdown
import matplotlib.figure as mplfig
import seaborn as sns
from fastapi import Request
from jinja2 import Undefined, pass_context
from jinja2.runtime import Context
from markupsafe import Markup
from plotly.graph_objects import Figure

from boredcharts.utils import uuid_to_urlid

logger = logging.getLogger("boredcharts")


def md_to_html(md: str) -> Markup:
    """Renders a Markdown as HTML."""
    return Markup(markdown.markdown(md))


SeabornGrid: TypeAlias = (
    sns.FacetGrid | sns.PairGrid | sns.JointGrid
)  # I think that's all of them


def to_html(fig: Figure | mplfig.Figure | alt.typing.ChartType | SeabornGrid) -> Markup:
    """Renders a Figure to an HTML string."""
    match fig:
        case Figure():
            return plotly_to_html(fig)
        case _ if isinstance(fig, alt.typing.ChartType):  # type: ignore[arg-type]
            # the above is correct on >=3.10, but mypy doesn't handle it: https://github.com/python/mypy/issues/17680
            # so we have to manually cast:
            fig = cast(alt.typing.ChartType, fig)
            return altair_to_html(fig)
        case mplfig.Figure():
            return mpl_to_html(fig)
        case _ if isinstance(fig, SeabornGrid):
            fig = cast(SeabornGrid, fig)
            return sns_to_html(fig)
        case _:
            raise ValueError(
                f"Input must be a Plotly/Matplotlib Figure, got {type(fig)}"
            )


def plotly_to_html(fig: Figure) -> Markup:
    """Renders a Plotly Figure as HTML."""
    return Markup(
        fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            default_height="100%",
            default_width="100%",
            config={
                "displaylogo": False,
                "responsive": True,
                "displayModeBar": False,
            },
        )
    )


def altair_to_html(chart: alt.typing.ChartType) -> Markup:
    """Renders an Altair Chart as HTML."""
    id_ = uuid_to_urlid(uuid.uuid4())
    figid = f"vis-{id_}"  # html id can't start with digit
    return Markup(
        chart.to_html(
            fullhtml=False,
            output_div=figid,
        )
    )


def mpl_to_html(fig: mplfig.Figure) -> Markup:
    """Renders a Matplotlib Chart as HTML."""
    with BytesIO() as buffer:
        fig.savefig(buffer, format="png", dpi=250)
        buffer.seek(0)
        png = buffer.read()
    png64 = base64.b64encode(png).decode("utf-8")

    title = fig.get_suptitle()
    if not title:
        titles = []
        for ax in fig.get_axes():
            if t := ax.get_title():
                titles.append(t)
        title = "; ".join(titles)

    return Markup(f"""<img src="data:image/png;base64,{png64}" alt="{title}">""")


def sns_to_html(fig: SeabornGrid) -> Markup:
    """Renders a Seaborn Chart as HTML."""
    return mpl_to_html(fig.figure)


@pass_context
def figure(
    context: Context,
    figure: str,
    *,
    css_class: str = "min-h-112 min-w-80",
    **kwargs: Any,
) -> Markup:
    """Jinja function to display a figure.

    Calls a figure endpoint and swaps-in the returned HTML snippet.

    e.g.:
    {{ figure("example_figure") }}
    {{ figure("example_figure_with_params", param_1="foo") }}
    """
    report = context.resolve("report")
    if not isinstance(report, Undefined):
        if not isinstance(report, str):
            raise ValueError(f"report must be a string, got {type(report)}")
        kwargs.update(report_name=report)

    request = context.resolve("request")
    if isinstance(request, Undefined):
        raise ValueError("request is not available in the context")
    if not isinstance(request, Request):
        raise ValueError(f"request must be a Request, got {type(request)}")

    url = request.url_for(figure).include_query_params(**kwargs)

    # note: using dedent to return a valid root-level element
    # note: markdown.markdown can't recognise multilne tags so we have to keep the root-level tag on the first line
    #   i.e.:
    #   <div
    #     class="flex flex-1 items-stretch"
    #   >
    #   is not recognised as a tag, so it would get wrapped in <p> tags, which we don't want
    return Markup(
        dedent(f"""
            <div hx-ext="response-targets" class="not-prose flex flex-1 items-stretch {css_class}">
                <figure
                    class="plotly-container min-h-0 min-w-0 flex-1"
                    hx-get="{url}"
                    hx-trigger="load"
                    hx-swap="innerHTML"
                    hx-target-error="find div"
                >
                    <div class="flex h-full w-full items-center justify-center bg-stone-100">
                        <p>loading...</p>
                    </div>
                </figure>
            </div>
        """).strip()
    )


def row(*figures: Markup) -> Markup:
    """Jinja function to display multiple figures in a single row.

    e.g.:
    {{
        row(
            figure("example_figure"),
            figure("example_figure_with_params", param_1="foo"),
        )
    }}
    """

    # Important:
    # ---
    # For HTML to be a valid block in markdown, it must be a root-level element.
    # This means there shouldn't be any leading whitespace for the first tag in the
    # returned string.
    # I'm guaranteeing that by pinning the fstring to the left, and using indent to
    # correctly format the inner HTML.
    # We could also just use strip on the whole thing and not bother with the indents,
    # but that would make the returned markup less readable.
    out = Markup(
        f"""
<div class="flex flex-wrap not-prose">
{indent("\n".join(figures), " " * 4)}
</div>
        """.strip()
    )
    logger.debug(out)
    return out
