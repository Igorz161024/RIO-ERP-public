import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from backend.main import app
from backend.auth import get_current_user


def override_get_current_user():
    class MockUser:
        id = 1
        username = "test"
        role = "admin"

    return MockUser()


app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_inventory_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/inventory/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_inventory_create():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/inventory/",
            json={
                "product": "Test Product",
                "quantity": 10,
                "batch": "TEST-001",
                "price": 100.0
            }
        )

    assert response.status_code == 200
    data = response.json()

    assert data["product"] == "Test Product"
    assert data["quantity"] == 10
    assert data["batch"] == "TEST-001"
    assert data["price"] == 100.0
