from pathlib import Path

from boredcharts.webapp import boredcharts
from fastapi import APIRouter
from fastapi.testclient import TestClient


def test_healthz() -> None:
    client = TestClient(
        boredcharts(
            pages=Path(__file__).parent / "pages",
            figure_router=APIRouter(),
        )
    )
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
