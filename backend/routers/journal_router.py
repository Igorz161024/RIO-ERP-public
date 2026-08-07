from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import journal
from backend.schemas import JournalSchema, JournalCreate, JournalUpdate
from backend.auth import get_current_user_role

router = APIRouter(
    prefix="/api/journal",
    tags=["Journal"]
)

@router.get("/", response_model=list[JournalSchema])
def read_journal(role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["accountant", "admin", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.query(journal.Journal).all()

@router.post("/", response_model=JournalSchema)
def create_journal(entry: JournalCreate, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["accountant", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    new_entry = journal.Journal(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{entry_id}", response_model=JournalSchema)
def update_journal(entry_id: int, entry: JournalUpdate, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["accountant", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(journal.Journal).filter(journal.Journal.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_journal(entry_id: int, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["accountant", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(journal.Journal).filter(journal.Journal.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
