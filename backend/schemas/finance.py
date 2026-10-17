from pydantic import BaseModel
from datetime import date
from typing import Optional

class FinanceBase(BaseModel):
    date: date
    account: str
    debit: float = 0
    credit: float = 0
    balance: float = 0
    description: Optional[str] = None

class FinanceCreate(FinanceBase):
    pass

class FinanceUpdate(BaseModel):
    date: Optional[date] = None
    account: Optional[str] = None
    debit: Optional[float] = None
    credit: Optional[float] = None
    balance: Optional[float] = None
    description: Optional[str] = None

class FinanceSchema(FinanceBase):
    id: int

    class Config:
        from_attributes = True

# --- Додаткові схеми для кастомних ендпоінтів ---
class FinanceEntry(BaseModel):
    account_id: int
    date: date
    operation: str
    amount: float
    status: str

class FinanceReportRequest(BaseModel):
    from_date: date
    to_date: date

class FinancePlotRequest(BaseModel):
    account_id: int
    from_date: date
    to_date: date
