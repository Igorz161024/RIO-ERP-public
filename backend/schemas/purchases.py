from pydantic import BaseModel
from typing import Optional


class PurchaseBase(BaseModel):
    supplier: str
    country: str

    product: str
    quantity: int
    price: float

    amount: float


class PurchaseCreate(PurchaseBase):
    pass


class PurchaseUpdate(BaseModel):
    supplier: Optional[str] = None
    country: Optional[str] = None

    product: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

    amount: Optional[float] = None


class PurchaseSchema(PurchaseBase):
    id: int

    class Config:
        from_attributes = True