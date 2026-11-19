from unittest.mock import patch

from frontend_rio.services.users import get_users


@patch("frontend_rio.services.users.httpx.get")
def test_get_users(mock_get):

    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "username": "testuser",
            "email": "test@test.com",
            "role": "user",
        }
    ]

    mock_get.return_value.raise_for_status.return_value = None

    data = get_users()

    assert len(data) == 1


@patch("frontend_rio.services.users.httpx.get")
def test_get_users_returns_list(mock_get):

    mock_get.return_value.json.return_value = []

    mock_get.return_value.raise_for_status.return_value = None

    data = get_users()

    assert isinstance(data, list)