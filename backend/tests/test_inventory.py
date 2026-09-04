# backend/tests/test_inventory.py

import pytest
from backend.database import SessionLocal
from backend.models.inventory import Inventory

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_inventory(db):
    new_item = Inventory(product="Item A", quantity=10, batch="B001")
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    assert new_item.id is not None
    assert new_item.quantity == 10

def test_read_inventory(db):
    item = db.query(Inventory).filter_by(product="Item A").first()
    assert item is not None
    assert item.product == "Item A"

def test_update_inventory(db):
    item = db.query(Inventory).filter_by(product="Item A").first()
    item.quantity = 20
    db.commit()
    db.refresh(item)
    assert item.quantity == 20

def test_delete_inventory(db):
    item = db.query(Inventory).filter_by(product="Item A").first()
    db.delete(item)
    db.commit()
    deleted = db.query(Inventory).filter_by(product="Item A").first()
    assert deleted is None
