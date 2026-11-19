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
async def test_legal_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/legal/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_legal_create():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/legal/",
            json={
                "contract": "Test Contract",
                "partner": "Test Partner",
                "status": "draft"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["contract"] == "Test Contract"
    assert data["partner"] == "Test Partner"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_legal_update_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.put(
            "/api/legal/999999",
            json={
                "status": "signed"
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_legal_delete_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/api/legal/999999"
        )

    assert response.status_code == 404