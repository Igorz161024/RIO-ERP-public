from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.journal import Journal
from backend.schemas.journal import JournalSchema, JournalCreate, JournalUpdate
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/journal",
    tags=["Journal"]
)

@router.get("/", response_model=list[JournalSchema])
def get_journal_entries(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Journal).all()

@router.get("/{entry_id}", response_model=JournalSchema)
def get_journal_entry(
    entry_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entry = db.query(Journal).filter(Journal.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return entry

@router.post("/", response_model=JournalSchema)
def create_journal_entry(
    entry: JournalCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_entry = Journal(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{entry_id}", response_model=JournalSchema)
def update_journal_entry(
    entry_id: int,
    entry: JournalUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_entry = db.query(Journal).filter(Journal.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    update_data = entry.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_entry, field, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_journal_entry(
    entry_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_entry = db.query(Journal).filter(Journal.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": f"Запис {entry_id} видалено"}
