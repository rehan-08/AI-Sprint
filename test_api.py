import pytest
from fastapi.testclient import TestClient
from api.routes import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_check_interactions():
    payload = {"ingredients": ["Aspirin", "Ibuprofen"]}
    response = client.post("/check-interactions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "interactions" in data
    assert "ingredient_details" in data   # new field present
    assert len(data["interactions"]) >= 1
    # Check disease mapping
    assert "Aspirin" in data["ingredient_details"]
    assert "Ibuprofen" in data["ingredient_details"]