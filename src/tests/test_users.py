import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app from your main file
# Assuming the structure is src/main.py
# and app is defined as "app".
from src.main import app
from src.config import engine
from src.models import Base

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_db():
    # Create tables before running tests
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after running all tests
    Base.metadata.drop_all(bind=engine)


def test_create_user():
    # Data for the new test user
    new_user = {
        "name": "TestUser",
        "email": "testuser@example.com",
        "password": "supersecret",
        "credits": 10
    }

    response = client.post("/users/", json=new_user)
    assert response.status_code == 200, response.text
    data = response.json()

    # Verify that the fields are correct
    assert data["email"] == "testuser@example.com"
    assert data["credits"] == 10
    assert "id" in data

    # Save the id for subsequent tests
    global created_user_id
    created_user_id = data["id"]


def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) > 0
    # Verify that the newly created user is in the list
    emails = [user["email"] for user in data]
    assert "testuser@example.com" in emails


def test_read_user_by_id():
    # Use the id saved in test_create_user
    response = client.get(f"/users/{created_user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == created_user_id
    assert data["email"] == "testuser@example.com"


def test_update_user_credits():
    updated_credits = 50
    response = client.put(f"/users/{created_user_id}/credits?new_credits={updated_credits}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["credits"] == updated_credits


def test_delete_user():
    response = client.delete(f"/users/{created_user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["detail"] == "User deleted successfully."

    # Verify that the user is no longer available
    get_response = client.get(f"/users/{created_user_id}")
    assert get_response.status_code == 404
