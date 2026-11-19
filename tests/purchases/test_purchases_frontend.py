from unittest.mock import patch

from frontend_rio.services.purchases import get_purchases


@patch("frontend_rio.services.purchases.httpx.get")
def test_get_purchases(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "supplier": "Test Supplier",
            "country": "Ukraine",
            "product": "Test Product",
            "quantity": 10,
            "price": 100.0,
            "amount": 1000.0,
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_purchases()

    assert len(data) == 1


@patch("frontend_rio.services.purchases.httpx.get")
def test_get_purchases_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_purchases()

    assert isinstance(data, list)