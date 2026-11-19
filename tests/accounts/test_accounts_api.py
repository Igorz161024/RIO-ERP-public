import uuid

import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from backend.main import app


@pytest.mark.asyncio
async def test_accounts_list():

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/api/accounts/")

    assert response.status_code in [200, 401]


@pytest.mark.asyncio
async def test_accounts_create_endpoint():

    unique_name = f"TestAccount_{uuid.uuid4().hex[:8]}"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.post(
            "/api/accounts/",
            json={
                "name": unique_name,
                "balance": 100.0,
            },
        )

    assert response.status_code in [200, 201, 401]


@pytest.mark.asyncio
async def test_accounts_update_endpoint():

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.put(
            "/api/accounts/999999",
            json={
                "balance": 200.0,
            },
        )

    assert response.status_code in [404, 401]


@pytest.mark.asyncio
async def test_accounts_delete_endpoint():

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.delete(
            "/api/accounts/999999"
        )

    assert response.status_code in [404, 401]