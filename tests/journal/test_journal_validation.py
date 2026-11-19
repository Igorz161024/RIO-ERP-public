from datetime import date

import pytest

from backend.schemas.journal import (
    JournalCreate,
    JournalUpdate,
)


def test_journal_create_valid():

    entry = JournalCreate(
        date=date.today(),
        operation="Sale",
        status="Completed",
        amount=100.0,
        account_id=1,
    )

    assert entry.operation == "Sale"


def test_journal_update_valid():

    entry = JournalUpdate(
        status="Updated"
    )

    assert entry.status == "Updated"


def test_journal_missing_operation():

    with pytest.raises(Exception):

        JournalCreate(
            date=date.today(),
            status="Completed",
            amount=100.0,
        )