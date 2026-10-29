
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


def test_dependency_graph_endpoint():
    response = client.get("/api/repositories/graph")

    assert response.status_code == 200

    data = response.json()

    assert data["total_nodes"] >= 1
    assert isinstance(data["edges"], list)


def test_change_impact_endpoint():
    response = client.post(
        "/api/repositories/impact",
        json={
            "target_file": "app/services/scanner.py"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["target_file"] == "app/services/scanner.py"
    assert data["total_affected"] >= 1


def test_change_impact_invalid_file():
    response = client.post(
        "/api/repositories/impact",
        json={
            "target_file": "nonexistent.py"
        },
    )

    assert response.status_code == 404
