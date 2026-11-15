import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from backend.main import app


@pytest.mark.asyncio
async def test_inventory_list():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        response = await ac.get("/api/inventory/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


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