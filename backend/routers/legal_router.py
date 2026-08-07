from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models
from backend.schemas import LegalSchema, LegalCreate, LegalUpdate
from backend.auth import get_current_user_role

router = APIRouter(
    prefix="/api/legal",
    tags=["Legal"]
)

# --- CRUD для Legal ---
@router.get("/", response_model=list[LegalSchema])
def read_legal(
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["lawyer", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.query(models.Legal).all()

@router.post("/", response_model=LegalSchema)
def create_legal(
    entry: LegalCreate,
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["lawyer", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    new_entry = models.Legal(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{entry_id}", response_model=LegalSchema)
def update_legal(
    entry_id: int,
    entry: LegalUpdate,
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["lawyer", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(models.Legal).filter(models.Legal.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_legal(
    entry_id: int,
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["lawyer", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(models.Legal).filter(models.Legal.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
