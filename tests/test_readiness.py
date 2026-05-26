from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_readiness():
    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json()["ready"] is True