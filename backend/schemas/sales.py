from pydantic import BaseModel
from typing import Optional

class SaleBase(BaseModel):
    client: str
    invoice: str
    amount: float

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    client: Optional[str] = None
    invoice: Optional[str] = None
    amount: Optional[float] = None

class SaleSchema(SaleBase):
    id: int

    class Config:
        from_attributes = True  # для Pydantic v2
