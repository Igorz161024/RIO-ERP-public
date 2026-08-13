from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.sales import Sale
from backend.schemas.sales import SaleSchema, SaleCreate, SaleUpdate
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"]
)

# --- CRUD для Sales ---
@router.get("/", response_model=list[SaleSchema])
def read_sales(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Sale).all()

@router.post("/", response_model=SaleSchema)
def create_sale(entry: SaleCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_entry = Sale(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{sale_id}", response_model=SaleSchema)
def update_sale(sale_id: int, entry: SaleUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
