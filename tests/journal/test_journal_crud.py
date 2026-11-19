from datetime import date

from backend.models.journal import Journal


def test_journal_model_create():
    entry = Journal(
        date=date.today(),
        operation="Sale",
        status="Completed",
        amount=100.0,
    )

    assert entry.operation == "Sale"


def test_journal_amount_type():
    entry = Journal(
        amount=100.0
    )

    assert isinstance(entry.amount, float)


def test_journal_status_type():
    entry = Journal(
        status="Completed"
    )

    assert isinstance(entry.status, str)