from app import schemas

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