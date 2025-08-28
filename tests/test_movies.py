import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel, Session
from app.main import app
from app.database import get_session
from app.models import Movie

# Use an in-memory SQLite DB for tests
TEST_DB_URL = "sqlite://"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})

@pytest.fixture(autouse=True)
def override_db():
    SQLModel.metadata.create_all(engine)
    def get_test_session():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_session] = get_test_session
    yield
    SQLModel.metadata.drop_all(engine)
    app.dependency_overrides.clear()

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_crud_flow():
    # Create
    payload = {
        "title": "The Shawshank Redemption",
        "director": "Frank Darabont",
        "release_year": 1994,
        "genre": "Drama",
        "rating": 9.3
    }
    r = client.post("/movies/", json=payload)
    assert r.status_code == 201
    created = r.json()
    movie_id = created["id"]
    assert created["title"] == payload["title"]

    # Get
    r = client.get(f"/movies/{movie_id}")
    assert r.status_code == 200
    assert r.json()["id"] == movie_id

    # List (pagination)
    r = client.get("/movies?offset=0&limit=10")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert any(m["id"] == movie_id for m in r.json())

    # Update
    upd = {"rating": 9.5}
    r = client.put(f"/movies/{movie_id}", json=upd)
    assert r.status_code == 200
    assert r.json()["rating"] == 9.5

    # Delete
    r = client.delete(f"/movies/{movie_id}")
    assert r.status_code == 204

    # Verify gone
    r = client.get(f"/movies/{movie_id}")
    assert r.status_code == 404

def test_validation_rating_bounds():
    bad = {
        "title": "X",
        "director": "Someone",
        "release_year": 2025,
        "genre": "Drama",
        "rating": 10.5   # invalid
    }
    r = client.post("/movies/", json=bad)
    assert r.status_code == 422

def test_update_not_found():
    r = client.put(f"/movies/99999", json={"title": "New"})
    assert r.status_code == 404