from pydantic import BaseModel
from typing import Optional

class PurchaseBase(BaseModel):
    supplier: str
    country: str
    amount: float

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseUpdate(BaseModel):
    supplier: Optional[str] = None
    country: Optional[str] = None
    amount: Optional[float] = None

class PurchaseSchema(PurchaseBase):
    id: int

    class Config:
        orm_mode = True
