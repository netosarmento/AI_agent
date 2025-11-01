from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_chat():
    response = client.post("/chat", json={"message": "Oi"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


# Teste Automático 