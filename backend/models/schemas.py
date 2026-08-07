from pydantic import BaseModel
from datetime import date
from typing import Optional

class JournalBase(BaseModel):
    date: date
    operation: str
    status: str
    amount: float
    entry_id: Optional[int] = None

class JournalCreate(JournalBase):
    """Схема для створення нового запису"""
    pass

class JournalRead(JournalBase):
    id: int

    class Config:
        orm_mode = True
