from textwrap import dedent, indent
from typing import Any

import markdown
from fastapi import Request
from jinja2 import Undefined, pass_context
from jinja2.runtime import Context
from markupsafe import Markup
from plotly.graph_objects import Figure


def to_html(fig: Figure) -> Markup:
    """Renders a Plotly Figure to an HTML string."""
    if not isinstance(fig, Figure):
        raise ValueError(f"Input must be a Plotly Figure, got {type(fig)}")
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


def md_to_html(md: str) -> Markup:
    """Renders a Markdown string to HTML."""
    return Markup(markdown.markdown(md))


@pass_context
def figure(
    context: Context,
    figure: str,
    *,
    css_class: str = "min-h-112 min-w-80",
    **kwargs: dict[str, Any],
) -> Markup:
    """"""
    report = context.resolve("report")
    if isinstance(report, Undefined):
        raise ValueError("report is not available in the context")
    if not isinstance(report, str):
        raise ValueError(f"report must be a string, got {type(report)}")

    request = context.resolve("request")
    if isinstance(request, Undefined):
        raise ValueError("request is not available in the context")
    if not isinstance(request, Request):
        raise ValueError(f"request must be a Request, got {type(request)}")

    url = request.url_for(figure, report_name=report).include_query_params(**kwargs)

    # note using dedent to return a valid root-level element
    return Markup(
        dedent(f"""
            <div
                hx-ext="response-targets"
                class="not-prose {css_class} flex flex-1 items-stretch"
            >
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
    """Combines multiple figures into a single row."""

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
    print(out)
    return out
