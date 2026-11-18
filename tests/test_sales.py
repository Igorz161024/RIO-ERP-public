import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from backend.main import app


@pytest.mark.asyncio
async def test_sales_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/sales/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_sale_create_missing_inventory():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/sales/",
            json={
                "client": "Test Client",
                "product": "NotExistingProduct",
                "quantity": 5,
                "price": 200.0,
                "amount": 1000.0
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_sale_update_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.put(
            "/api/sales/999999",
            json={
                "amount": 1200.0
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_sale_delete_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/api/sales/999999"
        )

    assert response.status_code == 404