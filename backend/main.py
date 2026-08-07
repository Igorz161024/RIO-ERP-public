from fastapi import FastAPI
from backend.routers import (
    accounts_router,
    journal_router,
    finance_router,
    legal_router,
    sales_router,
    inventory_router,
    purchases_router
)

app = FastAPI(
    title="Ріо ERP",
    description="ERP-система на FastAPI + PostgreSQL",
    version="1.0.0"
)


# ✅ Підключаємо всі роутери
app.include_router(accounts_router.router)
app.include_router(journal_router.router)
app.include_router(finance_router.router)
app.include_router(legal_router.router)
app.include_router(sales_router.router)
app.include_router(inventory_router.router)
app.include_router(purchases_router.router)
