# backend/tests/test_legal.py

import pytest
from backend.database import SessionLocal
from backend.models.legal import Legal

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

def test_create_legal(db):
    new_doc = Legal(contract="Contract A", partner="Partner1", status="draft")
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    assert new_doc.id is not None
    assert new_doc.status == "draft"

def test_read_legal(db):
    doc = db.query(Legal).filter_by(contract="Contract A").first()
    assert doc is not None
    assert doc.contract == "Contract A"

def test_update_legal(db):
    doc = db.query(Legal).filter_by(contract="Contract A").first()
    doc.status = "signed"
    db.commit()
    db.refresh(doc)
    assert doc.status == "signed"

def test_delete_legal(db):
    doc = db.query(Legal).filter_by(contract="Contract A").first()
    db.delete(doc)
    db.commit()
    deleted = db.query(Legal).filter_by(contract="Contract A").first()
    assert deleted is None
