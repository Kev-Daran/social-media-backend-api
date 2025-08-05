from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.main import app
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from app import models

SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        yield session


    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)



@pytest.fixture
def test_user(client):
    new_user = {"email" : "testuser@gmail.com", "password" : "testuserpassword"}
    res = client.post("/users/", json=new_user)

    assert res.status_code == 201
    user_data = res.json()
    user_data["password"] = new_user["password"]
    return user_data


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id" : test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
            **client.headers,
            "Authorization" : f"Bearer {token}"
            }
    
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts = [
        {"title" : "1st title", "content" : "first content", "owner_id" : test_user["id"]},
        {"title" : "2nd title", "content" : "second content", "owner_id" : test_user["id"]},
        {"title" : "3rd title", "content" : "third content", "owner_id" : test_user["id"]}
        ]
    
    def create_post_map(post):
        return models.Post(**post)

    post_map = map(create_post_map, posts)
    post_list = list(post_map)
    session.add_all(post_list)
    session.commit()

    posts = session.query(models.Post).all()

    return posts