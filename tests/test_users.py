import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from backend.main import app
from backend.auth import get_current_user


def override_get_current_user():
    class MockUser:
        id = 1
        username = "admin"
        role = "admin"

    return MockUser()


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_users_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/users/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/users/",
            json={
                "username": "test_user_ci",
                "email": "test_user_ci@example.com",
                "password": "123456",
                "role": "user"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "test_user_ci"
    assert data["email"] == "test_user_ci@example.com"
    assert data["role"] == "user"


@pytest.mark.asyncio
async def test_update_missing_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.put(
            "/api/users/999999",
            json={
                "username": "updated_user"
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_missing_user():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/api/users/999999"
        )

    assert response.status_code == 404