from app import schemas
from .database import client, session
import pytest
from app.config import settings
from jose import jwt

@pytest.fixture
def test_user(client):
    new_user = {"email" : "testuser@gmail.com", "password" : "testuserpassword"}
    res = client.post("/users/", json=new_user)

    assert res.status_code == 201
    user_data = res.json()
    user_data["password"] = new_user["password"]
    return user_data


def test_root(client):
    res = client.get("/")

    assert res.json().get('message') == "API is active"
    assert res.status_code == 200


def test_user_create(client):
    res = client.post("/users/", json={"email" : "hello123@gmail.com", "password" : "password123"})

    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username" : test_user["email"], "password" : test_user["password"]})
    token_data = schemas.Token(**res.json())
    
    payload = jwt.decode(token_data.access_token, settings.secret_key, settings.algorithm)

    assert payload.get("user_id") == test_user["id"]
    assert token_data.token_type == "bearer"
    assert res.status_code == 200