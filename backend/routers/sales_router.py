from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import sales
from backend.schemas import SaleSchema, SaleCreate, SaleUpdate
from backend.auth import get_current_user_role

router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"]
)

# --- CRUD для Sales ---
@router.get("/", response_model=list[SaleSchema])
def read_sales(role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["sales", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.query(sales.Sale).all()

@router.post("/", response_model=SaleSchema)
def create_sale(entry: SaleCreate, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["sales", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    new_entry = sales.Sale(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{sale_id}", response_model=SaleSchema)
def update_sale(sale_id: int, entry: SaleUpdate, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["sales", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(sales.Sale).filter(sales.Sale.id == sale_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, role: str = Depends(get_current_user_role), db: Session = Depends(get_db)):
    if role not in ["sales", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(sales.Sale).filter(sales.Sale.id == sale_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
