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
