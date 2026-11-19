from unittest.mock import patch

from frontend_rio.services.legal import get_legal


@patch("frontend_rio.services.legal.httpx.get")
def test_get_legal(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "contract": "Contract-001",
            "partner": "Partner Ltd",
            "status": "Active",
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_legal()

    assert len(data) == 1


@patch("frontend_rio.services.legal.httpx.get")
def test_get_legal_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_legal()

    assert isinstance(data, list)