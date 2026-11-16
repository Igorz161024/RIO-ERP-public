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
async def test_finance_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/finance/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_finance_create():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/finance/",
            json={
                "date": "2026-11-15",
                "account": "Cash",
                "debit": 100.0,
                "credit": 0.0,
                "balance": 100.0,
                "description": "Test finance entry"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["account"] == "Cash"
    assert data["debit"] == 100.0


@pytest.mark.asyncio
async def test_finance_update_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.put(
            "/api/finance/999999",
            json={
                "description": "updated"
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_finance_delete_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/api/finance/999999"
        )

    assert response.status_code == 404