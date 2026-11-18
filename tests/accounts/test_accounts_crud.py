from backend.models.accounts import Account


def test_account_model_create():

    account = Account(
        id=1,
        name="Cash",
        balance=1000.0,
    )

    assert account.id == 1
    assert account.name == "Cash"
    assert account.balance == 1000.0


def test_account_balance_type():

    account = Account(
        name="Bank",
        balance=500.5,
    )

    assert isinstance(account.balance, float)


def test_account_name_not_empty():

    account = Account(
        name="Main Account",
        balance=0.0,
    )

    assert account.name != ""