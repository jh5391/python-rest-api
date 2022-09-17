import pytest
from app import schemas


def test_get_all_replys(authorized_client, test_posts, test_replys):
    res = authorized_client.get(f"/replys/{test_posts[0].id}")

    def validate(reply):
        return schemas.Reply(**reply)

    replys_map = map(validate, res.json())
    replys_list = list(replys_map)

    assert len(res.json()) == len(test_replys)
    assert res.status_code == 200


def test_unauthorized_user_get_one_post_replys(client, test_posts):
    res = client.get(f"/replys/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_replys_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/replys/88888")
    assert res.status_code == 404


@pytest.mark.parametrize(
    "post_id, comment",
    [
        (1, "comment1"),
        (1, "comment2"),
        (1, "comment3"),
    ],
)
def test_create_reply(authorized_client, test_user, test_posts, post_id, comment):
    res = authorized_client.post(
        "/replys/", json={"post_id": post_id, "comment": comment}
    )

    created_reply = schemas.Reply(**res.json())
    assert res.status_code == 201
    assert created_reply.post_id == post_id
    assert created_reply.comment == comment
    assert created_reply.user_id == test_user["id"]


def test_unauthorized_user_create_reply(client, test_user, test_posts):
    res = client.post(
        "/replys/", json={"post_id": 1, "comment": "unauthorized_user_comment"}
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_reply(client, test_user, test_replys):
    res = client.delete(f"/replys/{test_replys[0].id}")
    assert res.status_code == 401


def test_delete_reply_success(authorized_client, test_user, test_replys):
    res = authorized_client.delete(f"/replys/{test_replys[0].id}")

    assert res.status_code == 204


def test_delete_reply_non_exist(authorized_client, test_user, test_replys):
    res = authorized_client.delete(f"/replys/8000000")

    assert res.status_code == 404


def test_delete_other_user_reply(authorized_client, test_user, test_replys2):
    res = authorized_client.delete(f"/replys/{test_replys2[0].id}")
    assert res.status_code == 403


def test_update_reply(authorized_client, test_user, test_posts, test_replys):
    data = {
        "post_id": test_posts[0].id,
        "comment": "updated comment",
    }
    res = authorized_client.put(f"/replys/{test_replys[0].id}", json=data)
    updated_reply = schemas.Reply(**res.json())
    assert res.status_code == 200
    assert updated_reply.post_id == data["post_id"]
    assert updated_reply.comment == data["comment"]


def test_update_other_user_reply(
    authorized_client, test_user, test_user2, test_posts, test_replys2
):
    data = {
        "post_id": test_posts[3].id,
        "comment": "updated comment",
    }
    res = authorized_client.put(f"/replys/{test_replys2[0].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_reply(client, test_user, test_replys):
    res = client.put(f"/replys/{test_replys[0].id}")
    assert res.status_code == 401


def test_update_reply_non_exist(authorized_client, test_user, test_posts):
    data = {
        "post_id": test_posts[0].id,
        "comment": "updated comment",
    }
    res = authorized_client.put(f"/replys/8000000", json=data)

    assert res.status_code == 404
