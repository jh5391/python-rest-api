from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.models import get_db
from app.models import Base
from app.oauth2 import create_access_token
from app import models
from sqlalchemy_utils import database_exists, create_database


SQLALCHEMY_DATABASE_URL = f"mysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    print("my session fixture ran")
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "user_id": test_user["id"],
        },
        {"title": "2nd title", "content": "2nd content", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "user_id": test_user2["id"]},
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts


@pytest.fixture
def test_replys(test_user, session, test_posts):
    replys_data = [
        {
            "post_id": f"{test_posts[0].id}",
            "comment": "first comment",
            "user_id": test_user["id"],
        },
        {
            "post_id": f"{test_posts[0].id}",
            "comment": "Second comment",
            "user_id": test_user["id"],
        },
        {
            "post_id": f"{test_posts[0].id}",
            "comment": "Third comment",
            "user_id": test_user["id"],
        },
    ]

    def create_reply_model(reply):
        return models.Reply(**reply)

    reply_map = map(create_reply_model, replys_data)
    replys = list(reply_map)

    session.add_all(replys)

    session.commit()
    replys = (
        session.query(models.Reply)
        .filter(models.Reply.post_id == test_posts[0].id)
        .all()
    )

    return replys


@pytest.fixture
def test_replys2(session, test_posts, test_user2):
    replys_data = [
        {
            "post_id": f"{test_posts[3].id}",
            "comment": "test_user2_comment",
            "user_id": test_user2["id"],
        },
    ]

    def create_reply_model(reply):
        return models.Reply(**reply)

    reply_map = map(create_reply_model, replys_data)
    replys = list(reply_map)

    session.add_all(replys)

    session.commit()
    replys = (
        session.query(models.Reply)
        .filter(models.Reply.post_id == test_posts[3].id)
        .all()
    )

    return replys
