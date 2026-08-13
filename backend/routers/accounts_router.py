from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.accounts import Account
from backend.schemas.accounts import AccountSchema, AccountCreate, AccountUpdate
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/accounts",
    tags=["Accounts"]
)

# --- CRUD для Accounts ---
@router.get("/", response_model=list[AccountSchema])
def read_accounts(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Account).all()

@router.post("/", response_model=AccountSchema)
def create_account(
    entry: AccountCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_entry = Account(**entry.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{account_id}", response_model=AccountSchema)
def update_account(
    account_id: int,
    entry: AccountUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_entry = db.query(Account).filter(Account.id == account_id).first()
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
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_entry = db.query(Account).filter(Account.id == account_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Запис видалено"}
