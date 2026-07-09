import pytest


async def test_signup_creates_user(client):
    response = await client.post(
        "/api/auth/signup",
        json={"email": "julian@example.com", "password": "supersecret", "display_name": "Julian"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "julian@example.com"
    assert "hashed_password" not in body


async def test_login_with_correct_credentials(client, create_user):
    await create_user(email="julian@example.com", password="supersecret")
    response = await client.post(
        "/api/auth/login",
        data={"username": "julian@example.com", "password": "supersecret"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_with_wrong_password(client, create_user):
    await create_user(email="julian@example.com", password="supersecret")
    response = await client.post(
        "/api/auth/login",
        data={"username": "julian@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401