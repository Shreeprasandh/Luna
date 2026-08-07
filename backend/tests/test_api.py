"""
Epsilon Test Sentinel — Automated API test suite covering FastAPI routes.
"""

import sys
import os

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "zero_token_waste" in data
    assert "system" in data
    assert "safety_switches" in data


def test_session_lifecycle():
    # Start session
    start_res = client.post("/session/start")
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]
    assert session_id is not None

    # End session
    end_res = client.post("/session/end", json={"session_id": session_id})
    assert end_res.status_code == 200
    assert end_res.json()["status"] == "ended"


def test_chat_invalid_session():
    res = client.post("/chat", json={"session_id": "invalid-session-id", "text": "Hello"})
    assert res.status_code == 404
