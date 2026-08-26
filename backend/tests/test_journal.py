def test_create_journal(db_session):
    from backend.models.journal import Journal
    j = Journal(date="2026-08-26", operation="TestOp", status="open", amount=500)
    db_session.add(j)
    db_session.commit()
    assert j.id is not None

def test_read_journal(db_session):
    from backend.models.journal import Journal
    j = db_session.query(Journal).filter_by(operation="TestOp").first()
    assert j.amount == 500

def test_update_journal(db_session):
    from backend.models.journal import Journal
    j = db_session.query(Journal).filter_by(operation="TestOp").first()
    j.amount = 750
    db_session.commit()
    updated = db_session.query(Journal).filter_by(operation="TestOp").first()
    assert updated.amount == 750

def test_delete_journal(db_session):
    from backend.models.journal import Journal
    j = db_session.query(Journal).filter_by(operation="TestOp").first()
    db_session.delete(j)
    db_session.commit()
    deleted = db_session.query(Journal).filter_by(operation="TestOp").first()
    assert deleted is None
