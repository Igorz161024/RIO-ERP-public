from pydantic import BaseModel
from typing import Optional


class EntryLineBase(BaseModel):
    journal_id: int
    account_id: int
    debit: float = 0.0
    credit: float = 0.0


class EntryLineCreate(EntryLineBase):
    pass


class EntryLineUpdate(BaseModel):
    journal_id: Optional[int] = None
    account_id: Optional[int] = None
    debit: Optional[float] = None
    credit: Optional[float] = None


class EntryLineSchema(EntryLineBase):
    id: int

    class Config:
        from_attributes = True