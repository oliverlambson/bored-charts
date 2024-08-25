from pathlib import Path

from boredcharts.router import FigureRouter
from boredcharts.webapp import boredcharts
from fastapi.testclient import TestClient


def test_healthz() -> None:
    client = TestClient(
        boredcharts(
            pages=Path(__file__).parent / "pages",
            figures=FigureRouter(),
        )
    )
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
