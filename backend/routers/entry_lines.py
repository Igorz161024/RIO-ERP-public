from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/api/entry_lines",
    tags=["entry_lines"]
)

@router.post("/", response_model=schemas.EntryLineSchema)
def create_entry_line(entry_line: schemas.EntryLineCreate, db: Session = Depends(get_db)):
    new_line = models.EntryLine(**entry_line.dict())
    db.add(new_line)
    db.commit()
    db.refresh(new_line)
    return new_line

@router.get("/{entry_line_id}", response_model=schemas.EntryLineSchema)
def read_entry_line(entry_line_id: int, db: Session = Depends(get_db)):
    line = db.query(models.EntryLine).filter(models.EntryLine.id == entry_line_id).first()
    if not line:
        raise HTTPException(status_code=404, detail="EntryLine not found")
    return line

@router.put("/{entry_line_id}", response_model=schemas.EntryLineSchema)
def update_entry_line(entry_line_id: int, entry_line: schemas.EntryLineUpdate, db: Session = Depends(get_db)):
    line = db.query(models.EntryLine).filter(models.EntryLine.id == entry_line_id).first()
    if not line:
        raise HTTPException(status_code=404, detail="EntryLine not found")
    for key, value in entry_line.dict(exclude_unset=True).items():
        setattr(line, key, value)
    db.commit()
    db.refresh(line)
    return line

@router.delete("/{entry_line_id}")
def delete_entry_line(entry_line_id: int, db: Session = Depends(get_db)):
    line = db.query(models.EntryLine).filter(models.EntryLine.id == entry_line_id).first()
    if not line:
        raise HTTPException(status_code=404, detail="EntryLine not found")
    db.delete(line)
    db.commit()
    return {"detail": "EntryLine deleted"}
