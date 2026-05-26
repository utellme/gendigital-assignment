from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_artifact_endpoint():
    response = client.get("/artifact")

    assert response.status_code == 200

    body = response.json()

    assert body["version"] == "v1"
    assert "features" in body