from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_chat_endpoint(mocked_auth):  # Assume mocked auth
    response = client.post("/api/chat", json={"message": "What is maternal health?"})
    assert response.status_code == 200
    assert "response" in response.json()
