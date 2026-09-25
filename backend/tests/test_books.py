import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture(name="session")
def fixture_session():
    sqlite_file_name = "data/test.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="book")
def book(client: TestClient):
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

def test_client(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"hello world!"}

def test_get_books(client: TestClient):
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_books_id(book, client: TestClient):
    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == book["id"]

    response = client.get("/books/42000")
    assert response.status_code == 404

    response = client.get("/books/toto")
    assert response.status_code == 422

def test_post_books(client: TestClient):
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


def test_patch_books_id(book, client: TestClient):
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

def test_delete_books_id(client: TestClient):
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