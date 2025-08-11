from app import schemas, models
import pytest


@pytest.fixture
def test_vote(session, test_user, test_posts):
    new_vote = models.Votes(post_id = test_posts[0].id, user_id = test_user["id"])
    session.add(new_vote)
    session.commit()

    return new_vote


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/votes/", json={"post_id" : test_posts[3].id, "dir" : 1})

    assert res.status_code == 201


def test_vote_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/votes/", json={"post_id" : test_vote.post_id, "dir" : 1})

    assert res.status_code == 409

def test_vote_delete(authorized_client, test_vote):
    res = authorized_client.post("/votes/", json={"post_id" : test_vote.post_id, "dir" : 0})

    assert res.status_code == 201

def test_vote_delete_nonexistent(authorized_client, test_posts):
    res = authorized_client.post("/votes/", json={"post_id" : test_posts[0].id, "dir" : 0})

    assert res.status_code == 404

def test_vote_nonexistent(authorized_client):
    res = authorized_client.post("/votes/", json={"post_id" : 347, "dir" : 1})

    assert res.status_code == 404


def test_vote_unauthorized(client, test_posts):
    res = client.post("/votes/", json={"post_id" : test_posts[0].id, "dir" : 1})

    assert res.status_code == 401