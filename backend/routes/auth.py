from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services import auth

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token({"sub": user.username, "role": user.role})
    refresh_token = auth.create_refresh_token(user, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    new_access_token = auth.refresh_access_token(db, refresh_token)
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(username: str, db: Session = Depends(get_db)):
    user = db.query(auth.User).filter(auth.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    auth.revoke_refresh_token(user, db)
    return {"detail": "Logged out successfully"}
