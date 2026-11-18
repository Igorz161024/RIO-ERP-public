import pytest

from backend.schemas.sales import (
    SaleCreate,
    SaleUpdate,
)


def test_sale_create_valid():

    sale = SaleCreate(
        client="Test Client",
        product="Test Product",
        quantity=5,
        price=200.0,
        amount=1000.0,
    )

    assert sale.client == "Test Client"


def test_sale_update_valid():

    sale = SaleUpdate(
        amount=1200.0,
    )

    assert sale.amount == 1200.0


def test_sale_missing_client():

    with pytest.raises(Exception):

        SaleCreate(
            product="Test Product",
            quantity=5,
            price=200.0,
            amount=1000.0,
        )