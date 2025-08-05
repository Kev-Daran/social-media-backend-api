from app import schemas
from app.config import settings
from jose import jwt
import pytest


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

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "testuserpassword", 403),
    ("testuser@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "testuserpassword", 403),
    ("testuser@gmail.com", None, 403) #oauth2 is converting None to "None" so its following original code logic
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username" : email, "password" : password})

    assert res.status_code == status_code