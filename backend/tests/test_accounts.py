def test_create_account(db_session):
    from backend.models.accounts import Account
    acc = Account(name="Test", balance=100)
    db_session.add(acc)
    db_session.commit()
    assert acc.id is not None

def test_read_account(db_session):
    from backend.models.accounts import Account
    acc = db_session.query(Account).filter_by(name="Test").first()
    assert acc.balance == 100

def test_update_account(db_session):
    from backend.models.accounts import Account
    acc = db_session.query(Account).filter_by(name="Test").first()
    acc.balance = 200
    db_session.commit()
    updated = db_session.query(Account).filter_by(name="Test").first()
    assert updated.balance == 200

def test_delete_account(db_session):
    from backend.models.accounts import Account
    acc = db_session.query(Account).filter_by(name="Test").first()
    db_session.delete(acc)
    db_session.commit()
    deleted = db_session.query(Account).filter_by(name="Test").first()
    assert deleted is None
