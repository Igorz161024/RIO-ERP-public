from unittest.mock import patch

from frontend_rio.services.finance import get_finance


@patch("frontend_rio.services.finance.httpx.get")
def test_get_finance(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "account": "Cash",
            "debit": 100.0,
            "credit": 0.0,
            "balance": 100.0,
            "date": "2026-11-15",
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_finance()

    assert len(data) == 1


@patch("frontend_rio.services.finance.httpx.get")
def test_get_finance_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_finance()

    assert isinstance(data, list)