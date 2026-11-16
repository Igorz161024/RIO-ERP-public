import pytest
from sqlalchemy.orm import Session

from backend.models.sales import Sale
from backend.database import engine, Base


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)

    session = Session(bind=engine)

    yield session

    session.close()


def test_create_sale(db_session):
    sale = Sale(
        client="Test Client",
        product="Test Product",
        quantity=5,
        price=200.0,
        amount=1000.0
    )

    db_session.add(sale)
    db_session.commit()
    db_session.refresh(sale)

    assert sale.id is not None


def test_read_sale(db_session):
    sale = db_session.query(Sale).filter_by(client="Test Client").first()

    assert sale is not None
    assert sale.product == "Test Product"


def test_update_sale(db_session):
    sale = db_session.query(Sale).filter_by(client="Test Client").first()

    sale.amount = 1200.0

    db_session.commit()
    db_session.refresh(sale)

    assert sale.amount == 1200.0


def test_delete_sale(db_session):
    sale = db_session.query(Sale).filter_by(client="Test Client").first()

    db_session.delete(sale)
    db_session.commit()

    deleted = db_session.query(Sale).filter_by(client="Test Client").first()

    assert deleted is None