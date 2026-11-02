from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db

from backend.models.sales import Sale
from backend.models.inventory import Inventory
from backend.models.journal import Journal
from backend.models.entry_lines import EntryLine

from backend.schemas.sales import (
    SaleSchema,
    SaleCreate,
    SaleUpdate,
)

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
    sale = (
        db.query(Sale)
        .filter(Sale.id == sale_id)
        .first()
    )

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
    inventory = (
        db.query(Inventory)
        .filter(Inventory.product == entry.product)
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Товар не знайдено на складі"
        )

    if inventory.quantity < entry.quantity:
        raise HTTPException(
            status_code=400,
            detail="Недостатньо товару на складі"
        )

    new_sale = Sale(
        client=entry.client,
        product=entry.product,
        quantity=entry.quantity,
        price=entry.price,
        amount=entry.amount
    )

    db.add(new_sale)
    db.flush()

    inventory.quantity -= entry.quantity

    journal = Journal(
        date=date.today(),
        operation="Sale",
        status="Completed",
        amount=entry.amount,
        account_id=3
    )

    db.add(journal)
    db.flush()

    debit_line = EntryLine(
        journal_id=journal.id,
        account_id=3,
        debit=entry.amount,
        credit=0
    )

    db.add(debit_line)

    credit_line = EntryLine(
        journal_id=journal.id,
        account_id=4,
        debit=0,
        credit=entry.amount
    )

    db.add(credit_line)

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
    db_sale = (
        db.query(Sale)
        .filter(Sale.id == sale_id)
        .first()
    )

    if not db_sale:
        raise HTTPException(
            status_code=404,
            detail="Запис не знайдено"
        )

    for field, value in entry.dict(exclude_unset=True).items():
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
    db_sale = (
        db.query(Sale)
        .filter(Sale.id == sale_id)
        .first()
    )

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