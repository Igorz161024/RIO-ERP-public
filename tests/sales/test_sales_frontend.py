from unittest.mock import patch

from frontend_rio.services.sales import get_sales


@patch("frontend_rio.services.sales.httpx.get")
def test_get_sales(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "client": "Test Client",
            "product": "Test Product",
            "quantity": 5,
            "price": 200.0,
            "amount": 1000.0,
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_sales()

    assert len(data) == 1


@patch("frontend_rio.services.sales.httpx.get")
def test_get_sales_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_sales()

    assert isinstance(data, list)