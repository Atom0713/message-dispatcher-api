import pytest
from fastapi.testclient import TestClient
from service.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
