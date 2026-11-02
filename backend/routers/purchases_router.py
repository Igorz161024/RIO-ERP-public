from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth import get_current_user
from backend.database import get_db

from backend.models.purchases import Purchase
from backend.models.inventory import Inventory
from backend.models.journal import Journal
from backend.models.entry_lines import EntryLine

from backend.schemas.purchases import (
    PurchaseSchema,
    PurchaseCreate,
    PurchaseUpdate,
)

router = APIRouter(
    prefix="/api/purchases",
    tags=["Purchases"]
)


@router.get("/", response_model=list[PurchaseSchema])
def get_purchases(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Purchase).all()


@router.get("/{item_id}", response_model=PurchaseSchema)
def get_purchase(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Purchase).filter(Purchase.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Запис не знайдено"
        )

    return item


@router.post("/", response_model=PurchaseSchema)
def create_purchase(
    entry: PurchaseCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # -------------------------
    # 1. Створення Purchase
    # -------------------------

    new_purchase = Purchase(
        supplier=entry.supplier,
        country=entry.country,
        product=entry.product,
        quantity=entry.quantity,
        price=entry.price,
        amount=entry.amount
    )

    db.add(new_purchase)
    db.flush()

    # -------------------------
    # 2. Створення Inventory
    # -------------------------

    inventory = Inventory(
        product=entry.product,
        quantity=entry.quantity,
        batch=f"PUR-{new_purchase.id}",
        price=entry.price
    )

    db.add(inventory)

    # -------------------------
    # 3. Створення Journal
    # -------------------------

    journal = Journal(
        date=date.today(),
        operation="Purchase",
        status="Completed",
        amount=entry.amount,
        account_id=1
    )

    db.add(journal)
    db.flush()

    # -------------------------
    # 4. Дебет
    # Дт Tovary
    # -------------------------

    debit_line = EntryLine(
        journal_id=journal.id,
        account_id=1,
        debit=entry.amount,
        credit=0
    )

    db.add(debit_line)

    # -------------------------
    # 5. Кредит
    # Кт Postachalnyky
    # -------------------------

    credit_line = EntryLine(
        journal_id=journal.id,
        account_id=2,
        debit=0,
        credit=entry.amount
    )

    db.add(credit_line)

    # -------------------------
    # 6. Збереження
    # -------------------------

    db.commit()
    db.refresh(new_purchase)

    return new_purchase


@router.put("/{item_id}", response_model=PurchaseSchema)
def update_purchase(
    item_id: int,
    entry: PurchaseUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(Purchase).filter(Purchase.id == item_id).first()

    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Запис не знайдено"
        )

    update_data = entry.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)

    return db_item


@router.delete("/{item_id}")
def delete_purchase(
    item_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(Purchase).filter(Purchase.id == item_id).first()

    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Запис не знайдено"
        )

    db.delete(db_item)
    db.commit()

    return {
        "detail": f"Запис {item_id} видалено"
    }