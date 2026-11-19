import uuid

import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from backend.main import app


@pytest.mark.asyncio
async def test_users_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/users/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_user_create():

    unique_id = uuid.uuid4().hex[:8]

    username = f"testuser_{unique_id}"
    email = f"test_{unique_id}@test.com"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/users/",
            json={
                "username": username,
                "email": email,
                "password": "123456",
                "role": "user"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == username
    assert data["email"] == email
    assert data["role"] == "user"


@pytest.mark.asyncio
async def test_user_update_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.put(
            "/api/users/999999",
            json={
                "role": "admin"
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_delete_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/api/users/999999"
        )

    assert response.status_code == 404