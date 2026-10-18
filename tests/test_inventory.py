import pytest
from httpx import AsyncClient
from backend.main import app

@pytest.mark.asyncio
async def test_inventory_list():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_inventory_create():
    new_item = {"name": "Test Product", "quantity": 10, "price": 99.99}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/inventory", json=new_item)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["quantity"] == 10
