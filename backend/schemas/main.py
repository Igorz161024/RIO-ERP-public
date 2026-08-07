from fastapi import FastAPI
from backend.schemas import (
    journal_router,
    finance_router,
    inventory_router,
    sales_router,
    purchases_router,
    legal_router,
    accounts_router
)

app = FastAPI(title="ERP Diplom Project")

# Підключення роутерів
app.include_router(journal_router.router, prefix="/api/journal", tags=["Journal"])
app.include_router(finance_router.router, prefix="/api/finance", tags=["Finance"])
app.include_router(inventory_router.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(sales_router.router, prefix="/api/sales", tags=["Sales"])
app.include_router(purchases_router.router, prefix="/api/purchases", tags=["Purchases"])
app.include_router(legal_router.router, prefix="/api/legal", tags=["Legal"])
app.include_router(accounts_router.router, prefix="/api/accounts", tags=["Accounts"])
