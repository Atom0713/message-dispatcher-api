from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_submit_message(client: TestClient):
    json_body = {"content": "dummy message"}
    response = client.post("/api/v1/recipients/dummy_recipient_id/messages", json=json_body)
    assert response.status_code == 200
    assert response.json() == {"delivery": "pending"}


def test_delete_message(client: TestClient):
    response = client.delete("/api/v1/recipients/dummy_recipient_id/messages/dummy_message_id")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_bulk_delete_messages(client: TestClient):
    json_body = {"messages": [{"content": "dummy message", "message_id": "dummy_message_id"}]}
    response = client.post("/api/v1/recipients/dummy_recipient_id/messages/delete", json=json_body)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_fetch_new_messages(client: TestClient):
    response = client.get("/api/v1/recipients/dummy_recipient_id/messages/new")
    assert response.status_code == 200
    assert response.json() == {"messages": [{"message_id": "dummy_message_id", "content": "dummy content"}]}


def test_fetch_messages_by_datetime_filter(client: TestClient):
    response = client.get(
        "/api/v1/recipients/dummy_recipient_id/messages?start_date=2025-09-01T10:00:00&end_date=2025-09-07T10:00:00"
    )
    assert response.status_code == 200
    assert response.json() == {"messages": [{"message_id": "dummy_message_id", "content": "dummy content"}]}


def test_fetch_messages_by_date_filter(client: TestClient):
    response = client.get("/api/v1/recipients/dummy_recipient_id/messages?start_date=2025-09-01&end_date=2025-09-07")
    assert response.status_code == 200
    assert response.json() == {"messages": [{"message_id": "dummy_message_id", "content": "dummy content"}]}
