from pydantic import BaseModel
from typing import Optional

class EntryLineBase(BaseModel):
    description: str
    amount: float
    journal_id: int

class EntryLineCreate(EntryLineBase):
    pass

class EntryLineUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    journal_id: Optional[int] = None

class EntryLineSchema(EntryLineBase):
    id: int

    class Config:
        from_attributes = True
