from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.sales import Sale
from backend.schemas.sales import (
    SaleSchema,
    SaleCreate,
    SaleUpdate,
)
from backend.auth import get_current_user


router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"]
)


@router.get("/", response_model=list[SaleSchema])
def get_sales(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Sale).all()


@router.get("/{sale_id}", response_model=SaleSchema)
def get_sale(
    sale_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Запис не знайдено"
        )

    return sale


@router.post("/", response_model=SaleSchema)
def create_sale(
    entry: SaleCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_sale = Sale(**entry.dict())

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale


@router.put("/{sale_id}", response_model=SaleSchema)
def update_sale(
    sale_id: int,
    entry: SaleUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_sale = db.query(Sale).filter(
        Sale.id == sale_id
    ).first()

    if not db_sale:
        raise HTTPException(
            status_code=404,
            detail="Запис не знайдено"
        )

    update_data = entry.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_sale, field, value)

    db.commit()
    db.refresh(db_sale)

    return db_sale


@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_sale = db.query(Sale).filter(
        Sale.id == sale_id
    ).first()

    if not db_sale:
        raise HTTPException(
            status_code=404,
            detail="Запис не знайдено"
        )

    db.delete(db_sale)
    db.commit()

    return {
        "detail": f"Запис {sale_id} видалено"
    }