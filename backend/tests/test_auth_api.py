import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup_creates_user(client: AsyncClient):
    response = await client.post(
        "/api/auth/signup",
        json={
            "email": "new@example.com",
            "password": "secret123",
            "display_name": "New User",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["email"] == "new@example.com"
    assert payload["display_name"] == "New User"


@pytest.mark.asyncio
async def test_login_returns_access_token(client: AsyncClient, create_user):
    await create_user(email="login@example.com", password="secret123", display_name="Login User")

    response = await client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
