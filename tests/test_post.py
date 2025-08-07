from app import schemas
import pytest

#   READ

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/all")

    def validate(post):
        schemas.PostOut(**post)

    posts = res.json()
    post_map = map(validate, posts)

    assert len(posts) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/all")

    assert res.status_code == 401

def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_get_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/234234")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[1].id}")
    
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[1].id

#   CREATE

@pytest.mark.parametrize("title, content, published", [
    ("Cool title!", "Cool content!!", True),    
    ("Top 10 best movies", "I don't really like movies", False),
    ("My favorite pokemon", "Torchic", True),
    ("Published", "Wait where is the argument?", False),
])
def test_create_posts(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title" : title, "content" : content, "published" : published})
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]

def test_create_post_published_default_value(authorized_client):
    res = authorized_client.post("/posts/", json={"title" : "Some title", "content" : "Some content"})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "Some title"
    assert created_post.content == "Some content"
    assert created_post.published == True

def test_unauthorized_create_post(client):
    res = client.post("/posts/", json={"title" : "Some title", "content" : "Some content"})

    assert res.status_code == 401

#   DELETE

def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_other_users_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403

def test_delete_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.delete("/posts/4583")

    assert res.status_code == 404

#   UPDATE

def test_unauthorized_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}", json={"title" : "Wow updated post!", "content" : "Now this is epic"})

    assert res.status_code == 401

def test_update_post(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json={"title" : "Wow updated post!", "content" : "Now this is epic"})
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == "Wow updated post!"
    assert updated_post.content == "Now this is epic"

def test_update_other_users_post(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json={"title" : "Wow updated post!", "content" : "Now this is epic"})

    assert res.status_code == 403

def test_update_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.put("/posts/4583", json={"title" : "Wow updated post!", "content" : "Now this is epic"})

    assert res.status_code == 404

