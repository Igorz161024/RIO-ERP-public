import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from jose import JWTError, jwt

from backend.database import SessionLocal, get_db
from backend.services.auth import authenticate_user, create_access_token, get_password_hash
from backend.routers import auth, entry_lines

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
# Підключення роутерів
# -------------------------------
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(entry_lines.router, prefix="/entry_lines", tags=["entry_lines"])

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

# JWT конфігурація
# -------------------------------
load_dotenv(dotenv_path=".env.prod")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365  # 365 днів

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

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
        new_item_data = item.dict()
        if prefix == "users" and "password" in new_item_data:
            new_item_data["password_hash"] = get_password_hash(new_item_data.pop("password"))
        new_item = model(**new_item_data)
        db.add(new_item); db.commit(); db.refresh(new_item)
        return new_item

    @app.put(f"/api/{prefix}/{{item_id}}", response_model=schema)
    def update_item(item_id: int, item: update_schema, current_user: dict = Depends(get_current_user)):
        db = SessionLocal()
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Not Found")
        update_data = item.dict(exclude_unset=True)
        if prefix == "users" and "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit(); db.refresh(db_item)
        return db_item

    @app.delete(f"/api/{prefix}/{{item_id}}")
    def delete_item(item_id: int, current_user: dict = Depends(get_current_user)):
        db = SessionLocal()
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Not Found")
        db.delete(db_item)
        db.commit()
        return {"detail": f"{prefix.capitalize()} deleted"}

# -------------------------------
# Реєстрація CRUD для всіх модулів
# -------------------------------
crud_routes(Account, AccountSchema, AccountCreate, AccountUpdate, "accounts")
crud_routes(Journal, JournalSchema, JournalCreate, JournalUpdate, "journal")
crud_routes(Finance, FinanceSchema, FinanceCreate, FinanceUpdate, "finance")
crud_routes(Inventory, InventorySchema, InventoryCreate, InventoryUpdate, "inventory")
crud_routes(Sale, SaleSchema, SaleCreate, SaleUpdate, "sales")
crud_routes(Legal, LegalSchema, LegalCreate, LegalUpdate, "legal")
crud_routes(Purchase, PurchaseSchema, PurchaseCreate, PurchaseUpdate, "purchases")
crud_routes(User, UserSchema, UserCreate, UserUpdate, "users")

# -------------------------------
# Точка входу
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=7000)




