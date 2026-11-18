import pytest

from backend.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
)


def test_inventory_create_valid():

    item = InventoryCreate(
        product="Test Product",
        quantity=10,
        batch="TEST-001",
        price=100.0,
    )

    assert item.product == "Test Product"


def test_inventory_update_valid():

    item = InventoryUpdate(
        quantity=20,
    )

    assert item.quantity == 20


def test_inventory_missing_product():

    with pytest.raises(Exception):

        InventoryCreate(
            quantity=10,
            batch="TEST-001",
            price=100.0,
        )