import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from backend.database import SessionLocal, get_db

# -------------------------------
# Ініціалізація FastAPI
# -------------------------------
app = FastAPI(title="RIO-ERP Backend", version="1.0.0")

# -------------------------------
# Налаштування CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Healthcheck endpoint
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------------
# Імпорти моделей
# -------------------------------
from backend.models.accounts import Account
from backend.models.journal import Journal
from backend.models.finance import Finance
from backend.models.inventory import Inventory
from backend.models.sales import Sale
from backend.models.legal import Legal
from backend.models.purchases import Purchase
from backend.models.user import User
from backend.models.entry_lines import EntryLine

# -------------------------------
# Імпорти схем
# -------------------------------
from backend.schemas.accounts import AccountSchema, AccountCreate, AccountUpdate
from backend.schemas.journal import JournalSchema, JournalCreate, JournalUpdate
from backend.schemas.finance import FinanceSchema, FinanceCreate, FinanceUpdate
from backend.schemas.inventory import InventorySchema, InventoryCreate, InventoryUpdate
from backend.schemas.sales import SaleSchema, SaleCreate, SaleUpdate
from backend.schemas.legal import LegalSchema, LegalCreate, LegalUpdate
from backend.schemas.purchases import PurchaseSchema, PurchaseCreate, PurchaseUpdate
from backend.schemas.user import UserSchema, UserCreate, UserUpdate
from backend.schemas.entry_lines import EntryLineSchema, EntryLineCreate, EntryLineUpdate

# -------------------------------
# Імпорти роутерів
# -------------------------------
from backend.routers import users_router, journal_router, finance_router
app.include_router(users_router.router)
app.include_router(journal_router.router)
app.include_router(finance_router.router)
from backend.routers import inventory_router
app.include_router(inventory_router.router)

# -------------------------------
# Імпорти авторизації
# -------------------------------
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth import get_current_user, authenticate_user, create_access_token

# -------------------------------
# Ендпоінт для отримання токена
# -------------------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------------
# CRUD для модулів (крім Users)
# -------------------------------
def crud_routes(model, schema, create_schema, update_schema, prefix: str):
    @app.get(f"/api/{prefix}/", response_model=list[schema])
    def get_items(current_user: User = Depends(get_current_user)):
        db = SessionLocal()
        return [schema.model_validate(obj) for obj in db.query(model).all()]

    @app.post(f"/api/{prefix}/", response_model=schema)
    def create_item(item: create_schema, current_user: User = Depends(get_current_user)):
        db = SessionLocal()
        new_item = model(**item.dict())
        db.add(new_item); db.commit(); db.refresh(new_item)
        return new_item

    @app.put(f"/api/{prefix}/{{item_id}}", response_model=schema)
    def update_item(item_id: int, item: update_schema, current_user: User = Depends(get_current_user)):
        db = SessionLocal()
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Not Found")
        for field, value in item.dict(exclude_unset=True).items():
            setattr(db_item, field, value)
        db.commit(); db.refresh(db_item)
        return db_item

    @app.delete(f"/api/{prefix}/{{item_id}}")
    def delete_item(item_id: int, current_user: User = Depends(get_current_user)):
        db = SessionLocal()
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Not Found")
        db.delete(db_item); db.commit()
        return {"detail": f"{prefix.capitalize()} deleted"}

# -------------------------------
# Реєстрація CRUD для модулів
# -------------------------------
crud_routes(Account, AccountSchema, AccountCreate, AccountUpdate, "accounts")
crud_routes(Sale, SaleSchema, SaleCreate, SaleUpdate, "sales")
crud_routes(Legal, LegalSchema, LegalCreate, LegalUpdate, "legal")
crud_routes(Purchase, PurchaseSchema, PurchaseCreate, PurchaseUpdate, "purchases")
crud_routes(EntryLine, EntryLineSchema, EntryLineCreate, EntryLineUpdate, "entry_lines")

# -------------------------------
# Точка входу
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=7000)
