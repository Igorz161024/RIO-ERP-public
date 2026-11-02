from pydantic import BaseModel
from typing import Optional


class SaleBase(BaseModel):
    client: str
    product: str
    quantity: int
    price: float
    amount: float


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    client: Optional[str] = None
    product: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    amount: Optional[float] = None


class SaleSchema(SaleBase):
    id: int

    class Config:
        from_attributes = True