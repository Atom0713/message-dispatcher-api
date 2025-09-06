from fastapi.testclient import TestClient
from src.service.app import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
