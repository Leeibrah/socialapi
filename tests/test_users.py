import pytest
from jose import jwt
from app import schemas

from app.config import settings


def test_root(client):
    res = client.get("/")

    print(res.json().get('message'))

    result = res.json().get('message')
    status_code = res.status_code

    assert result == 'Python API Application made using FastAPI!'
    assert status_code == 200

# Create a user from test_user
# Login a user using test_user credentials
def test_login_user(client, test_user):
    res = client.post(
        "/login", json = {"email": test_user['email'], "password": test_user['password']}
    )

    login_res = schemas.tokens.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id =  payload.get("user_id")

    assert res.status_code == 200
    assert id == test_user['id']
    assert login_res.token_type == "bearer"

# Create a user from scratch
def test_create_user(client):
    res = client.post("/users/", json = {"name": "Lee", "email": "lee@lee.com", "password": "lee"})

    created_user = schemas.users.User(**res.json())

    assert created_user.email == 'lee@lee.com'
    assert res.status_code == 201


@pytest.mark.parametrize("email, password, status_code", [
    ("ken@ken.com", "ken", 403),
    ("admin@admin.com", "admin1", 403),
    ("admin@admin.com", None, 422),
    (None, "admin1", 422),
])
def test_incorrect_login(client, email, password, status_code):
    # res = client.post("/login", json = {"email": "lee@lee.com", "password": "wrongpass"})
    res = client.post("/login", json = {"email": email, "password": password})

    # print(res.status_code)
    # print(res)
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid email or password"