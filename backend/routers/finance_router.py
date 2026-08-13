from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models.finance import Finance
from backend.models.accounts import Account
from backend.models.journal import Journal
from backend.schemas.finance import FinanceSchema, FinanceCreate, FinanceUpdate
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/finance",
    tags=["Finance"]
)

# --- CRUD для Finance ---
@router.get("/", response_model=list[FinanceSchema])
def read_finance(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Finance).all()

@router.post("/", response_model=FinanceSchema)
def create_finance(entry: FinanceCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_entry = Finance(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{entry_id}", response_model=FinanceSchema)
def update_finance(entry_id: int, entry: FinanceUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Finance).filter(Finance.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_finance(entry_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_entry = db.query(Finance).filter(Finance.id == entry_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}

# --- Баланс по рахунку ---
@router.get("/balance/{account_id}")
def get_balance(account_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    total = db.query(func.sum(Journal.amount)).filter(Journal.account_id == account_id).scalar() or 0
    return {"account_id": account_id, "balance": account.balance + total}

# --- Спецмаршрути ---
@router.post("/add_entry")
def add_entry(entry: dict, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    new_entry = Journal(
        account_id=entry["account_id"],
        date=entry["date"],
        operation=entry["operation"],
        amount=entry["amount"],
        status=entry["status"]
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"detail": "Entry added", "id": new_entry.id}

@router.get("/report")
def report(from_date: str, to_date: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(Journal).filter(
        Journal.date >= from_date,
        Journal.date <= to_date
    ).all()
    return records

@router.get("/plot")
def plot(account_id: int, from_date: str, to_date: str, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    data = db.query(Journal.date, Journal.amount).filter(
        Journal.account_id == account_id,
        Journal.date >= from_date,
        Journal.date <= to_date
    ).all()
    return {"account_id": account_id, "points": [{"date": d, "amount": a} for d, a in data]}
