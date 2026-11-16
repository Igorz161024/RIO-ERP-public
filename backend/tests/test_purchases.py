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
    purchase = Purchase(
        supplier="Test Supplier",
        country="UA",
        product="Test Product",
        quantity=10,
        price=150.0,
        amount=1500.0
    )

    db_session.add(purchase)
    db_session.commit()
    db_session.refresh(purchase)

    assert purchase.id is not None


def test_read_purchase(db_session):
    purchase = db_session.query(Purchase).filter_by(
        supplier="Test Supplier"
    ).first()

    assert purchase is not None
    assert purchase.country == "UA"
    assert purchase.product == "Test Product"


def test_update_purchase(db_session):
    purchase = db_session.query(Purchase).filter_by(
        supplier="Test Supplier"
    ).first()

    purchase.amount = 2000.0

    db_session.commit()
    db_session.refresh(purchase)

    assert purchase.amount == 2000.0


def test_delete_purchase(db_session):
    purchase = db_session.query(Purchase).filter_by(
        supplier="Test Supplier"
    ).first()

    db_session.delete(purchase)
    db_session.commit()

    deleted = db_session.query(Purchase).filter_by(
        supplier="Test Supplier"
    ).first()

    assert deleted is None