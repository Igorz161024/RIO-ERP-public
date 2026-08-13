from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.purchases import Purchase
from backend.schemas.purchases import PurchaseSchema, PurchaseCreate, PurchaseUpdate
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/purchases",
    tags=["Purchases"]
)

# --- CRUD для Purchases ---
@router.get("/", response_model=list[PurchaseSchema])
def read_purchases(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Purchase).all()

@router.post("/", response_model=PurchaseSchema)
def create_purchase(entry: PurchaseCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_entry = Purchase(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{purchase_id}", response_model=PurchaseSchema)
def update_purchase(purchase_id: int, entry: PurchaseUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{purchase_id}")
def delete_purchase(purchase_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
