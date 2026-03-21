"""Tests for chat routes"""

from tests.conftest import client


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_create_session():
    """Test creating a new chat session"""
    response = client.post("/api/chat/session/create")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["mode"] == "gentle_guide"


def test_get_available_modes():
    """Test getting available modes"""
    response = client.get("/api/chat/modes")
    assert response.status_code == 200
    data = response.json()
    assert "modes" in data
    assert "default" in data
    assert len(data["modes"]) == 4
