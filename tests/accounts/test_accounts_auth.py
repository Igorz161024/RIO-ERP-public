import pytest

from backend.auth import create_access_token
from backend.auth import get_current_user
from fastapi import HTTPException


def test_create_token():

    token = create_access_token(
        {
            "sub": "admin",
            "role": "admin",
        }
    )

    assert token is not None
    assert isinstance(token, str)


def test_invalid_token():

    with pytest.raises(HTTPException):

        get_current_user("invalid_token")