import os
from pathlib import Path

from analysis import cars, elasticity, medals, penguins, population
from boredcharts import boredcharts

pages = Path(__file__).parent / "pages"
app = boredcharts(
    pages=pages,
    figures=[
        elasticity.figures,
        medals.figures,
        cars.figures,
        population.figures,
        penguins.figures,
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
