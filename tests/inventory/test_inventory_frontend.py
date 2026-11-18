from unittest.mock import patch

from frontend_rio.services.inventory import get_inventory


@patch("frontend_rio.services.inventory.httpx.get")
def test_get_inventory(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "product": "Test Product",
            "quantity": 10,
            "batch": "TEST-001",
            "price": 100.0,
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_inventory()

    assert len(data) == 1


@patch("frontend_rio.services.inventory.httpx.get")
def test_get_inventory_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_inventory()

    assert isinstance(data, list)