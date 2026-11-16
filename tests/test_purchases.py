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
async def test_purchases_list():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/purchases/")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_purchase_create():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/purchases/",
            json={
                "supplier": "Test Supplier",
                "country": "Ukraine",
                "product": "Test Product",
                "quantity": 10,
                "price": 100.0,
                "amount": 1000.0
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["supplier"] == "Test Supplier"
    assert data["product"] == "Test Product"
    assert data["amount"] == 1000.0


@pytest.mark.asyncio
async def test_purchase_update_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.put(
            "/api/purchases/999999",
            json={
                "supplier": "Updated Supplier"
            }
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_purchase_delete_missing():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/api/purchases/999999"
        )

    assert response.status_code == 404