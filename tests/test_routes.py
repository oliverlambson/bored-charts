from pathlib import Path

from boredcharts.router import BCRouter
from boredcharts.webapp import boredcharts
from fastapi.testclient import TestClient


def test_healthz() -> None:
    client = TestClient(
        boredcharts(
            pages=Path(__file__).parent / "pages",
            figure_router=BCRouter(),
        )
    )
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
