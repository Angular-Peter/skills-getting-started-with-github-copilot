import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed for in-memory activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())

def test_signup_for_activity():
    # Arrange
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()

def test_signup_duplicate():
    # Arrange
    activity = next(iter(client.get("/activities").json().keys()))
    email = "duplicate@example.com"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"].lower().find("already signed up") != -1
