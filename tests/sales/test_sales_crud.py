from backend.models.sales import Sale


def test_sale_model_create():

    sale = Sale(
        id=1,
        client="Test Client",
        product="Test Product",
        quantity=5,
        price=200.0,
        amount=1000.0,
    )

    assert sale.client == "Test Client"


def test_sale_quantity_type():

    sale = Sale(
        client="Test Client",
        product="Test Product",
        quantity=5,
        price=200.0,
        amount=1000.0,
    )

    assert isinstance(sale.quantity, int)


def test_sale_amount_type():

    sale = Sale(
        client="Test Client",
        product="Test Product",
        quantity=5,
        price=200.0,
        amount=1000.0,
    )

    assert isinstance(sale.amount, float)