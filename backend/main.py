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

# # -------------------------------
# Імпорти роутерів
# -------------------------------

import backend.routers.users_router as users_router
import backend.routers.journal_router as journal_router
import backend.routers.finance_router as finance_router
import backend.routers.inventory_router as inventory_router
import backend.routers.sales_router as sales_router
import backend.routers.purchases_router as purchases_router
import backend.routers.accounts_router as accounts_router
import backend.routers.legal_router as legal_router
import backend.routers.entry_lines as entry_lines

app.include_router(users_router.router)
app.include_router(journal_router.router)
app.include_router(finance_router.router)
app.include_router(inventory_router.router)
app.include_router(sales_router.router)
app.include_router(purchases_router.router)
app.include_router(accounts_router.router)
app.include_router(legal_router.router)
app.include_router(entry_lines.router)
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

# -------------------------------
# Точка входу
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=7000)
