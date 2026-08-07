from pydantic import BaseModel
from datetime import date
from typing import Optional

# ================= Journal =================
class JournalBase(BaseModel):
    date: date
    operation: str
    status: str
    amount: float
    entry_id: Optional[int] = None

class JournalCreate(JournalBase):
    pass

class JournalUpdate(JournalBase):
    pass

class JournalRead(JournalBase):
    id: int
    class Config:
        from_attributes = True


# ================= Finance =================
class FinanceBase(BaseModel):
    date: date
    debit: str
    credit: str
    amount: float
    desc: Optional[str] = None

class FinanceCreate(FinanceBase):
    pass

class FinanceUpdate(FinanceBase):
    pass

class FinanceRead(FinanceBase):
    id: int
    class Config:
        from_attributes = True


# ================= Inventory =================
class InventoryBase(BaseModel):
    product: str
    quantity: int
    batch: str

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(InventoryBase):
    pass

class InventoryRead(InventoryBase):
    id: int
    class Config:
        from_attributes = True


# ================= Purchases =================
class PurchaseBase(BaseModel):
    date: date
    supplier: str
    amount: float
    desc: Optional[str] = None

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseUpdate(PurchaseBase):
    pass

class PurchaseRead(PurchaseBase):
    id: int
    class Config:
        from_attributes = True


# ================= Sales =================
class SaleBase(BaseModel):
    date: date
    customer: str
    amount: float
    desc: Optional[str] = None

class SaleCreate(SaleBase):
    pass

class SaleUpdate(SaleBase):
    pass

class SaleRead(SaleBase):
    id: int
    class Config:
        from_attributes = True


# ================= Legal =================
class LegalBase(BaseModel):
    doc_id: str
    title: str
    status: str

class LegalCreate(LegalBase):
    pass

class LegalUpdate(LegalBase):
    pass

class LegalRead(LegalBase):
    id: int
    class Config:
        from_attributes = True
