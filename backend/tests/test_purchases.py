import pytest
from sqlalchemy.orm import Session
from backend.models.purchases import Purchase
from backend.database import engine, Base

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    yield session
    session.close()

def test_create_purchase(db_session):
    purchase = Purchase(supplier="Test Supplier", country="UA", amount=1500.75)
    db_session.add(purchase)
    db_session.commit()
    assert purchase.id is not None

def test_read_purchase(db_session):
    purchase = db_session.query(Purchase).filter_by(supplier="Test Supplier").first()
    assert purchase is not None
    assert purchase.country == "UA"

def test_update_purchase(db_session):
    purchase = db_session.query(Purchase).filter_by(supplier="Test Supplier").first()
    purchase.amount = 2000.00
    db_session.commit()
    updated = db_session.query(Purchase).filter_by(supplier="Test Supplier").first()
    assert updated.amount == 2000.00

def test_delete_purchase(db_session):
    purchase = db_session.query(Purchase).filter_by(supplier="Test Supplier").first()
    db_session.delete(purchase)
    db_session.commit()
    deleted = db_session.query(Purchase).filter_by(supplier="Test Supplier").first()
    assert deleted is None
