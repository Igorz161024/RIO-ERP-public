from backend.models.purchases import Purchase


def test_purchase_model_create():
    purchase = Purchase(
        supplier="Test Supplier",
        country="Ukraine",
        product="Test Product",
        quantity=10,
        price=100.0,
        amount=1000.0,
    )

    assert purchase.supplier == "Test Supplier"


def test_purchase_quantity_type():
    purchase = Purchase(
        quantity=10
    )

    assert isinstance(purchase.quantity, int)


def test_purchase_amount_type():
    purchase = Purchase(
        amount=1000.0
    )

    assert isinstance(purchase.amount, float)