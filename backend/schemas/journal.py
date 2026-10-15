from pydantic import BaseModel
from datetime import date
from typing import Optional

class JournalBase(BaseModel):
    date: date
    operation: str
    status: str
    amount: float

class JournalCreate(JournalBase):
    account_id: Optional[int] = None

class JournalUpdate(BaseModel):
    date: Optional[date] = None
    operation: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[float] = None
    account_id: Optional[int] = None

class JournalSchema(JournalBase):
    id: int
    account_id: Optional[int] = None   # ← додати сюди

    class Config:
        from_attributes = True
