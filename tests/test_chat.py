from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_chat_rejects_empty_question():
    response = client.post("/api/chat", json={"question": "   ", "history": []})
    assert response.status_code == 400


def test_chat_rejects_missing_question_field():
    response = client.post("/api/chat", json={"history": []})
    assert response.status_code == 422
