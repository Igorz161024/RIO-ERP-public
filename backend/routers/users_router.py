from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.schemas.user import UserSchema, UserCreate, UserUpdate
from backend.auth import get_current_user, get_password_hash

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserSchema])
def read_users(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(User).all()

@router.post("/", response_model=UserSchema)
def create_user(
    entry: UserCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_entry = User(
        username=entry.username,
        email=entry.email,
        password_hash=get_password_hash(entry.password),
        role=entry.role
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    entry: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_entry = db.query(User).filter(User.id == user_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    for key, value in entry.dict(exclude_unset=True).items():
        setattr(db_entry, key, value)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_entry = db.query(User).filter(User.id == user_id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    db.delete(db_entry)
    db.commit()
    return {"detail": "Користувача видалено"}
