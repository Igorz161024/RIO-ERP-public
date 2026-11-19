import pytest

from backend.schemas.purchases import (
    PurchaseCreate,
    PurchaseUpdate,
)


def test_purchase_create_valid():

    purchase = PurchaseCreate(
        supplier="Test Supplier",
        country="Ukraine",
        product="Test Product",
        quantity=10,
        price=100.0,
        amount=1000.0,
    )

    assert purchase.supplier == "Test Supplier"


def test_purchase_update_valid():

    purchase = PurchaseUpdate(
        supplier="Updated Supplier"
    )

    assert purchase.supplier == "Updated Supplier"


def test_purchase_missing_supplier():

    with pytest.raises(Exception):

        PurchaseCreate(
            country="Ukraine",
            product="Test Product",
            quantity=10,
            price=100.0,
            amount=1000.0,
        )