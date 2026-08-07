from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import inventory
from backend.schemas import InventorySchema, InventoryCreate, InventoryUpdate
from backend.auth import get_current_user_role

router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)

# --- CRUD для Inventory ---
@router.get("/", response_model=list[InventorySchema])
def read_inventory(role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["storekeeper", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.query(inventory.Inventory).all()

@router.post("/", response_model=InventorySchema)
def create_inventory(entry: InventoryCreate, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["storekeeper", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    new_entry = inventory.Inventory(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{item_id}", response_model=InventorySchema)
def update_inventory(item_id: int, entry: InventoryUpdate, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["storekeeper", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(inventory.Inventory).filter(inventory.Inventory.id == item_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{item_id}")
def delete_inventory(item_id: int, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["storekeeper", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(inventory.Inventory).filter(inventory.Inventory.id == item_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
