from datetime import date
import pytest

from backend.schemas.finance import (
    FinanceCreate,
    FinanceUpdate,
)


def test_finance_create_valid():

    entry = FinanceCreate(
        date=date.today(),
        account="Cash",
        debit=100.0,
        credit=0.0,
        balance=100.0,
        description="Test",
    )

    assert entry.account == "Cash"


def test_finance_update_valid():

    entry = FinanceUpdate(
        description="Updated",
    )

    assert entry.description == "Updated"


def test_finance_missing_account():

    with pytest.raises(Exception):

        FinanceCreate(
            date=date.today(),
            debit=100.0,
        )