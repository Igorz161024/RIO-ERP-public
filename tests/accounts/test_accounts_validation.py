import pytest

from backend.schemas.accounts import (
    AccountCreate,
    AccountUpdate,
)


def test_account_create_valid():

    account = AccountCreate(
        name="Cash",
        balance=100.0,
    )

    assert account.name == "Cash"
    assert account.balance == 100.0


def test_account_update_balance():

    account = AccountUpdate(
        balance=500.0,
    )

    assert account.balance == 500.0


def test_account_update_name():

    account = AccountUpdate(
        name="Updated",
    )

    assert account.name == "Updated"


def test_account_create_missing_name():

    with pytest.raises(Exception):

        AccountCreate(
            balance=100.0
        )