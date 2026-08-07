from fastapi import APIRouter, HTTPException
from typing import List
from backend.schemas.journal import JournalSchema, JournalCreate, JournalUpdate

router = APIRouter()

# Тимчасове сховище (замість БД)
fake_db: List[dict] = [
    {"id": 1, "date": "2026-05-21", "operation": "Test", "status": "ok", "amount": 100}
]

# GET: список записів
@router.get("/", response_model=List[JournalSchema])
def get_journal_entries():
    return fake_db

# GET: отримати запис за id
@router.get("/{entry_id}", response_model=JournalSchema)
def get_journal_entry(entry_id: int):
    for entry in fake_db:
        if entry["id"] == entry_id:
            return entry
    raise HTTPException(status_code=404, detail="Запис не знайдено")

# POST: створення нового запису
@router.post("/", response_model=JournalSchema)
def create_journal_entry(entry: JournalCreate):
    new_id = max([e["id"] for e in fake_db]) + 1 if fake_db else 1
    new_entry = {"id": new_id, **entry.dict()}
    fake_db.append(new_entry)
    return new_entry

# PUT: оновлення запису (часткове)
@router.put("/{entry_id}", response_model=JournalSchema)
def update_journal_entry(entry_id: int, entry: JournalUpdate):
    for idx, existing in enumerate(fake_db):
        if existing["id"] == entry_id:
            updated_entry = {**existing, **entry.dict(exclude_unset=True)}
            fake_db[idx] = updated_entry
            return updated_entry
    raise HTTPException(status_code=404, detail="Запис не знайдено")

# DELETE: видалення запису
@router.delete("/{entry_id}", response_model=dict)
def delete_journal_entry(entry_id: int):
    for idx, existing in enumerate(fake_db):
        if existing["id"] == entry_id:
            fake_db.pop(idx)
            return {"message": f"Запис {entry_id} видалено"}
    raise HTTPException(status_code=404, detail="Запис не знайдено")
