from datetime import date

from backend.models.finance import Finance


def test_finance_model_create():

    entry = Finance(
        id=1,
        date=date.today(),
        account="Cash",
        debit=100.0,
        credit=0.0,
        balance=100.0,
    )

    assert entry.account == "Cash"


def test_finance_debit_type():

    entry = Finance(
        date=date.today(),
        account="Cash",
        debit=100.0,
    )

    assert isinstance(entry.debit, float)


def test_finance_credit_type():

    entry = Finance(
        date=date.today(),
        account="Cash",
        credit=50.0,
    )

    assert isinstance(entry.credit, float)