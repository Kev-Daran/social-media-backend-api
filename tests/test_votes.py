from app import schemas

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/votes/", json={"post_id" : test_posts[3].id, "dir" : 1})