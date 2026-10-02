"""Tests for the health endpoint."""
import os
import sys

# Ensure the repo root is on the path when running pytest from any directory.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient

from api.index import app

client = TestClient(app)


def test_health_status_ok() -> None:
    """GET /api/health returns 200 with status == 'ok'."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "env" in data
