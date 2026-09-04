# backend/tests/test_finance.py

import pytest
from datetime import date
from backend.database import SessionLocal
from backend.models.finance import Finance

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_finance(db):
    new_tx = Finance(
        account="Main",
        balance=1000,
        description="Initial deposit",
        date=date.today()   # ← додаємо дату
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    assert new_tx.id is not None
    assert new_tx.balance == 1000

def test_read_finance(db):
    tx = db.query(Finance).filter_by(account="Main").first()
    assert tx is not None
    assert tx.balance == 1000

def test_update_finance(db):
    tx = db.query(Finance).filter_by(account="Main").first()
    tx.balance = 1500
    db.commit()
    db.refresh(tx)
    assert tx.balance == 1500

def test_delete_finance(db):
    tx = db.query(Finance).filter_by(account="Main").first()
    db.delete(tx)
    db.commit()
    deleted = db.query(Finance).filter_by(account="Main").first()
    assert deleted is None
