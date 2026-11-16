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
async def test_journal_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/journal/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_journal_create():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/journal/",
            json={
                "date": "2026-11-16",
                "operation": "Test operation",
                "status": "completed",
                "amount": 1000,
                "account_id": 1
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["operation"] == "Test operation"
    assert data["amount"] == 1000


@pytest.mark.asyncio
async def test_journal_update_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.put(
            "/api/journal/999999",
            json={
                "status": "updated"
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_journal_delete_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/api/journal/999999"
        )

    assert response.status_code == 404