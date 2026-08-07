from pydantic import BaseModel
from datetime import date
from typing import Optional

class JournalBase(BaseModel):
    date: date
    operation: str
    status: str
    amount: float

class JournalCreate(JournalBase):
    pass

class JournalUpdate(BaseModel):
    date: Optional[date] = None
    operation: Optional[str] = None
    status: Optional[str] = None
    amount: Optional[float] = None

class JournalSchema(JournalBase):
    id: int

    class Config:
        from_attributes = True  # для Pydantic v2
