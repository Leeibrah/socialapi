import pytest
from typing import List
from app import schemas


@pytest.mark.parametrize("title, content, published", [
    ("Title Un", "C'est le titre un", True),
    ("Title Duex", "C'est le titre duex", True),
    ("Title Trois", "C'est le titre trois", True),
    ("Title Quatre", "C'est le titre quatre", False),
    ("Title Cinq", "C'est le titre cinq", True)
])
def t_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json = {
        "title": title,
        "content": content,
        "published": published,
    })

    created_post = schemas.posts.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user.id == test_user['id']



def test_create_post_default_published_true(authorized_client, test_user):

    res = authorized_client.post("/posts/", json = {
        "title": "title 1",
        "content": "content of title 1",
    })

    created_post = schemas.posts.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "title 1"
    assert created_post.content == "content of title 1"
    assert created_post.published == True
    assert created_post.user.id == test_user['id']


def test_get_all_posts(authorized_client, test_posts):
# def t_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.posts.PostwithVote(**post)

    posts_map = map(validate, res.json())
    post_list = list(posts_map)
    print(list(posts_map))
    print(test_posts[0].id)
    print(post_list[0].Post.id)

    # assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert post_list[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_posts(client, test_posts):
# def t_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/loggedin/user")

    print(res.status_code)
    assert res.status_code == 401



def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    print(res.status_code)
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/88')

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    print(res.json())

    post = schemas.posts.PostwithVote(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.published == test_posts[0].published





def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json = {
        "title": "title 1",
        "content": "content of title 1",
    })

    print(res.status_code)
    assert res.status_code == 401


def test_unathorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    print(res.status_code)
    assert res.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204



def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/67")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    # assert res.status_code == 403
    assert res.status_code == 204


def test_update_post(authorized_client, test_user, test_posts):

    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)

    updated_post = schemas.posts.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):

    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)

    assert res.status_code == 403


def test_unathorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")

    print(res.status_code)
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):

    data = {
        "title": "Updated Title",
        "content": "Updated Content",
        "id": test_posts[3].id
    }

    res = authorized_client.put(f"/posts/67", json = data)

    assert res.status_code == 404