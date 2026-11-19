from unittest.mock import patch

from frontend_rio.services.journal import get_journal


@patch("frontend_rio.services.journal.httpx.get")
def test_get_journal(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "date": "2026-01-01",
            "operation": "Sale",
            "status": "Completed",
            "amount": 100.0,
            "account_id": 1,
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_journal()

    assert len(data) == 1


@patch("frontend_rio.services.journal.httpx.get")
def test_get_journal_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_journal()

    assert isinstance(data, list)