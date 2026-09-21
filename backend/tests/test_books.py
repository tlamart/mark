import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def book():
    data = {
        "title": "test_title",
        "author": "test_author",
        "current_page": 0,
        "total_page": 42
    }
    response = client.post("/books", json=data)
    book = response.json()

    yield book

    client.delete(f"/books/{book['id']}")

def test_client():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"hello world!"}

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_books_id(book):
    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == book["id"]

    response = client.get("/books/42000")
    assert response.status_code == 404

    response = client.get("/books/toto")
    assert response.status_code == 422

def test_post_books():
    data = {
        "title": "test_title",
        "author": "test_author",
        "current_page": 0,
        "total_page": 42
    }
    response = client.post("/books", json=data)
    book = response.json()
    client.delete(f"/books/{book['id']}")
    assert response.status_code == 200
    assert book["title"] == "test_title"

    data["author"] = 42
    response = client.post("/books", json=data)
    print(response.json())
    assert response.status_code == 422


def test_patch_books_id(book):
    data = {
        "current_page": 42,
        "reading_time": 42
    }
    response = client.patch(f"/books/{book['id']}", json=data)
    assert response.status_code == 200
    assert response.json()["current_page"] == 42
    assert response.json()["reading_time"] == 42

    data["current_page"] = "test"
    response = client.patch(f"/books/{book['id']}", json=data)
    assert response.status_code == 422

def test_delete_books_id():
    data = {
            "title": "test_title",
            "author": "test_author",
            "current_page": 0,
            "total_page": 42
        }
    book = client.post("/books", json=data).json()
    response = client.delete(f"/books/{book['id']}")
    assert response.status_code == 200
    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 404

