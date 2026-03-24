from dispatcher.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app=app)

def test_book_endpoint_without_auth():
    response = client.get("/books")

    assert response.status_code == 401
    assert response.json() == {"detail": "Yetkisiz erişim"}