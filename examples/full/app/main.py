import os
from pathlib import Path

from boredcharts import boredcharts

from app import elasticity, medals, population

pages = Path(__file__).parent.parent.absolute() / "pages"
app = boredcharts(
    pages=pages,
    figure_router=[
        elasticity.router,
        medals.router,
        population.router,
    ],
)


def entrypoint() -> None:
    import uvicorn

    uvicorn.run(
        f"{__name__}:app",
        host=os.getenv("UVICORN_HOST", "127.0.0.1"),
        port=4000,
        reload=os.getenv("UVICORN_RELOAD", "false").upper() == "TRUE",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    entrypoint()
