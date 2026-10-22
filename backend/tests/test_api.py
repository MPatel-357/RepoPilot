
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_repository_scan_endpoint():
    response = client.post("/api/repositories/scan")

    assert response.status_code == 200

    data = response.json()

    assert data["total_files"] >= 1
    assert isinstance(data["files"], list)
    assert isinstance(data["errors"], list)
