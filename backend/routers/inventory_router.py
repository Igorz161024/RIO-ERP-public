from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.inventory import Inventory
from backend.schemas.inventory import InventorySchema, InventoryCreate, InventoryUpdate
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)

# --- CRUD для Inventory ---
@router.get("/", response_model=list[InventorySchema])
def read_inventory(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@router.post("/", response_model=InventorySchema)
def create_inventory(entry: InventoryCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_entry = Inventory(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{item_id}", response_model=InventorySchema)
def update_inventory(item_id: int, entry: InventoryUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{item_id}")
def delete_inventory(item_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
