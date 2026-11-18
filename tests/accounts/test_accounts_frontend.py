from unittest.mock import patch

from frontend_rio.services.accounts import get_accounts


@patch("frontend_rio.services.accounts.httpx.get")
def test_get_accounts(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "name": "Cash",
            "balance": 1000.0,
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_accounts()

    assert len(data) == 1
    assert data[0]["name"] == "Cash"


@patch("frontend_rio.services.accounts.httpx.get")
def test_get_accounts_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_accounts()

    assert isinstance(data, list)