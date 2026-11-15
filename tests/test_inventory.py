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
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        response = await ac.get("/api/inventory/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_inventory_create():
    new_item = {
        "name": "Test Product",
        "quantity": 10,
        "price": 99.99
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/api/inventory/",
            json=new_item
        )

    assert response.status_code in [200, 201]