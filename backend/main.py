from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# SQLAlchemy ORM
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

# Pydantic
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:4568@rio_erp_db:5432/erp_diplom"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# -------------------------------
# ORM-моделі
# -------------------------------
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    journals = relationship("Journal", back_populates="account")

class Journal(Base):
    __tablename__ = "journal"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    operation = Column(String, nullable=False)
    status = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="journals")

# -------------------------------
# Pydantic-схеми
# -------------------------------
class AccountSchema(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True   # заміна orm_mode у Pydantic v2

class JournalSchema(BaseModel):
    id: int
    date: datetime
    operation: str
    status: str
    amount: int
    account_id: int
    class Config:
        from_attributes = True

# -------------------------------
# JWT конфігурація
# -------------------------------
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -------------------------------
# Генерація токена
# -------------------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "1234":
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": form_data.username, "role": "admin", "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# -------------------------------
# Перевірка токена
# -------------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# -------------------------------
# CRUD для accounts (ORM)
# -------------------------------
@app.get("/api/accounts/", response_model=list[AccountSchema])
def get_accounts(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return db.query(Account).all()

@app.post("/api/accounts/", response_model=AccountSchema)
def create_account(account: dict, current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    new_acc = Account(name=account["name"])
    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)
    return new_acc

# -------------------------------
# CRUD для journal (ORM)
# -------------------------------
@app.get("/api/journal/", response_model=list[JournalSchema])
def get_journal(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    return db.query(Journal).all()

# -------------------------------
# Тестовий код для volume‑перевірки
# -------------------------------
@app.on_event("startup")
def startup_event():
    print("⚡ Volume test OK — main.py оновлено")
    db = SessionLocal()
    try:
        existing = db.query(Account).filter_by(name="Test Account").first()
        if not existing:
            test_acc = Account(name="Test Account")
            db.add(test_acc)
            db.commit()
            test_journal = Journal(operation="Init", status="ok", amount=100, account_id=test_acc.id)
            db.add(test_journal)
            db.commit()
            print(f"Створено Account ID={test_acc.id} з Journal ID={test_journal.id}")
    except IntegrityError:
        db.rollback()
    finally:
        db.close()

# -------------------------------
# Підключення нового роутера users
# -------------------------------
from backend.routers import users_router
app.include_router(users_router.router)

