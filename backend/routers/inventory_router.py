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

@router.get("/", response_model=list[InventorySchema])
def get_inventory_items(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Inventory).all()

@router.get("/{item_id}", response_model=InventorySchema)
def get_inventory_item(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return item

@router.post("/", response_model=InventorySchema)
def create_inventory_item(
    entry: InventoryCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_item = Inventory(**entry.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.put("/{item_id}", response_model=InventorySchema)
def update_inventory_item(
    item_id: int,
    entry: InventoryUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    update_data = entry.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_inventory_item(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_item)
    db.commit()
    return {"detail": f"Запис {item_id} видалено"}
