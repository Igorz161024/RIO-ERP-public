from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import accounts
from backend.schemas import AccountSchema, AccountCreate, AccountUpdate
from backend.auth import get_current_user_role

router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"]
)

# Dependency для отримання сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD для Accounts ---
@router.get("/", response_model=list[AccountSchema])
def read_accounts(
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["accountant", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return db.query(accounts.Account).all()

@router.post("/", response_model=AccountSchema)
def create_account(
    entry: AccountCreate,
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["accountant", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    new_entry = accounts.Account(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{account_id}", response_model=AccountSchema)
def update_account(
    account_id: int,
    entry: AccountUpdate,
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["accountant", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(accounts.Account).filter(accounts.Account.id == account_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["accountant", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    db_entry = db.query(accounts.Account).filter(accounts.Account.id == account_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
