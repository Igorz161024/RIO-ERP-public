from backend.models.inventory import Inventory


def test_inventory_model_create():

    item = Inventory(
        id=1,
        product="Test Product",
        quantity=10,
        batch="TEST-001",
        price=100.0,
    )

    assert item.product == "Test Product"


def test_inventory_quantity_type():

    item = Inventory(
        product="Test Product",
        quantity=10,
        batch="TEST-001",
        price=100.0,
    )

    assert isinstance(item.quantity, int)


def test_inventory_price_type():

    item = Inventory(
        product="Test Product",
        quantity=10,
        batch="TEST-001",
        price=100.0,
    )

    assert isinstance(item.price, float)