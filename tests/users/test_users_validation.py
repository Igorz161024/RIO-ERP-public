import pytest

from backend.schemas.user import (
    UserCreate,
    UserUpdate,
)


def test_user_create_valid():

    user = UserCreate(
        username="testuser",
        email="test@test.com",
        password="123456",
        role="user",
    )

    assert user.username == "testuser"


def test_user_update_valid():

    user = UserUpdate(
        role="admin"
    )

    assert user.role == "admin"


def test_user_missing_username():

    with pytest.raises(Exception):

        UserCreate(
            email="test@test.com",
            password="123456",
            role="user",
        )