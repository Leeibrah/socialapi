from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command

import pytest
from app.oauth2 import create_access_token

from app.main import app
from app import models

from app.config import settings
from app.database import Base, get_db

# client = TestClient(app)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("Start session fixture")
    # Drop tables in DB
    Base.metadata.drop_all(bind=engine)
    # Create tables in DB
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    # Test your code
    yield TestClient(app)

# 
@pytest.fixture
def test_user(client):
    user_data = {"name": "Admin", "email": "admin@admin.com", "password": "admin"}

    res = client.post("/users/", json = user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "name": "Mike", "email": "mike@mike.com", "password": "mike",
        "name": "Tom", "email": "tom@tom.com", "password": "tom",
    }

    res = client.post("/users/", json = user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


# 
@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

# 
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


#
@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "First Title",
            "content": "This is the first content.",
            "published": True,
            "user_id": test_user['id']
        },
        {
            "title": "Second Title",
            "content": "This is the second content.",
            "published": True,
            "user_id": test_user['id']
        },
        {
            "title": "Third Title",
            "content": "This is the third content.",
            "published": False,
            "user_id": test_user['id']
        },
        {
            "title": "Fourth Title",
            "content": "This is the Fourth content.",
            "published": False,
            "user_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()

    return posts