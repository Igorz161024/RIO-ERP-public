from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# SQLAlchemy ORM
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Pydantic
from pydantic import BaseModel
from typing import Optional

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
    balance = Column(Float, default=0.0)
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

class Finance(Base):
    __tablename__ = "finance"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, nullable=False)
    total = Column(Float, nullable=False)

class Legal(Base):
    __tablename__ = "legal"
    id = Column(Integer, primary_key=True, index=True)
    case = Column(String, nullable=False)
    status = Column(String, nullable=False)

class Purchases(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, nullable=False)
    cost = Column(Float, nullable=False)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

# -------------------------------
# Pydantic-схеми
# -------------------------------
class AccountBase(BaseModel):
    name: str
    balance: float
class AccountCreate(AccountBase): pass
class AccountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[float] = None
class AccountSchema(AccountBase):
    id: int
    class Config: from_attributes = True

class JournalBase(BaseModel):
    operation: str
    status: str
    amount: int
    account_id: int
class JournalCreate(JournalBase): pass
class JournalUpdate(BaseModel):
    operation: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[int] = None
class JournalSchema(JournalBase):
    id: int
    date: datetime
    class Config: from_attributes = True

class FinanceBase(BaseModel):
    description: str
    amount: float
class FinanceCreate(FinanceBase): pass
class FinanceUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
class FinanceSchema(FinanceBase):
    id: int
    class Config: from_attributes = True

class InventoryBase(BaseModel):
    item: str
    quantity: int
class InventoryCreate(InventoryBase): pass
class InventoryUpdate(BaseModel):
    item: Optional[str] = None
    quantity: Optional[int] = None
class InventorySchema(InventoryBase):
    id: int
    class Config: from_attributes = True

class SalesBase(BaseModel):
    product: str
    total: float
class SalesCreate(SalesBase): pass
class SalesUpdate(BaseModel):
    product: Optional[str] = None
    total: Optional[float] = None
class SalesSchema(SalesBase):
    id: int
    class Config: from_attributes = True

class LegalBase(BaseModel):
    case: str
    status: str
class LegalCreate(LegalBase): pass
class LegalUpdate(BaseModel):
    case: Optional[str] = None
    status: Optional[str] = None
class LegalSchema(LegalBase):
    id: int
    class Config: from_attributes = True

class PurchasesBase(BaseModel):
    item: str
    cost: float
class PurchasesCreate(PurchasesBase): pass
class PurchasesUpdate(BaseModel):
    item: Optional[str] = None
    cost: Optional[float] = None
class PurchasesSchema(PurchasesBase):
    id: int
    class Config: from_attributes = True

class UsersBase(BaseModel):
    username: str
    email: str
class UsersCreate(UsersBase): pass
class UsersUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
class UsersSchema(UsersBase):
    id: int
    class Config: from_attributes = True

# -------------------------------
# JWT конфігурація
# -------------------------------
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.prod")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "1234":
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": form_data.username, "role": "admin"}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

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
# CRUD для всіх модулів
# -------------------------------
def crud_routes(model, schema, create_schema, update_schema, prefix: str):
    @app.get(f"/api/{prefix}/", response_model=list[schema])
    def get_items(current_user: dict = Depends(get_current_user)):
        db = SessionLocal()
        return [schema.model_validate(obj) for obj in db.query(model).all()]

    @app.post(f"/api/{prefix}/", response_model=schema)
    def create_item(item: create_schema, current_user: dict = Depends(get_current_user)):
        db = SessionLocal()
        new_item = model(**item.dict())
        db.add(new_item); db.commit(); db.refresh(new_item)
        return new_item

    @app.put(f"/api/{prefix}/{{item_id}}", response_model=schema)
    def update_item(item_id: int, item: update_schema, current_user: dict = Depends(get_current_user)):
        db = SessionLocal()
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item: raise HTTPException(status_code=404, detail="Not Found")
        for field, value in item.dict(exclude_unset=True).items():
            setattr(db_item, field, value)
        db.commit(); db.refresh(db_item)
        return db_item

    @app.delete(f"/api/{prefix}/{{item_id}}")
    def delete_item(item_id: int, current_user: dict = Depends(get_current_user)):
        db = SessionLocal()
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item: raise HTTPException(status_code=404, detail="Not Found")
        db.delete(db_item); db.commit()
        return {"detail": f"{prefix.capitalize()} deleted"}

# Реєстрація CRUD для всіх модулів
crud_routes(Account, AccountSchema, AccountCreate, AccountUpdate, "accounts")
crud_routes(Journal, JournalSchema, JournalCreate, JournalUpdate, "journal")
crud_routes(Finance, FinanceSchema, FinanceCreate, FinanceUpdate, "finance")
crud_routes(Inventory, InventorySchema, InventoryCreate, InventoryUpdate, "inventory")
crud_routes(Sales, SalesSchema, SalesCreate, SalesUpdate, "sales")
crud_routes(Legal, LegalSchema, LegalCreate, LegalUpdate, "legal")
crud_routes(Purchases, PurchasesSchema, PurchasesCreate, PurchasesUpdate, "purchases")
crud_routes(Users, UsersSchema, UsersCreate, UsersUpdate, "users")



