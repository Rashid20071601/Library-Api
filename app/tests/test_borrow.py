import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

# Клиент для тестирования API
client = TestClient(app)

# JWT токен авторизованного пользователя (библиотекаря)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NDg3ODY1ODF9.DPnKu2UvDF3ejoSE608CEw6mTSuAT5jSDq3D5xoa2C4"
headers = {"Authorization": f"Bearer {token}"}


# Тест: читатель не может держать более 3-х книг одновременно
def test_reader_cannot_borrow_more_than_3_books():
    # Предполагается, что reader_id=1 и книги с id 1,2,3,4 существуют и доступны
    for book_id in [1, 2, 3]:
        response = client.post(
            "/borrow",
            json={"reader_id": 1, "book_id": book_id},
            headers=headers
        )
        assert response.status_code == 201

    # Попытка взять 4-ю книгу — должна вернуть ошибку
    response = client.post(
        "/borrow",
        json={"reader_id": 1, "book_id": 4},
        headers=headers
    )
    assert response.status_code == 400
    assert "максимально допустимое количество книг" in response.text


# Тест: нельзя взять книгу, если copies == 0
def test_borrow_book_when_none_available():
    # Предполагается, что book_id=5 существует, но copies = 0
    response = client.post(
        "/borrow",
        json={"reader_id": 1, "book_id": 5},
        headers=headers
    )
    assert response.status_code == 400
    assert "Нет доступных экземпляров книги" in response.text


# Тест: защищённый эндпоинт требует токен
def test_protected_route_requires_auth():
    # Без токена — должна быть ошибка 401
    response = client.get("/readers")
    assert response.status_code == 401

    # С токеном — успех
    response = client.get("/readers", headers=headers)
    assert response.status_code == 200
