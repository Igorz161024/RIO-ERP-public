from pydantic import BaseModel
from typing import Optional

class InventoryBase(BaseModel):
    product: str
    quantity: int
    batch: str
    price: float   # ← додано

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    product: Optional[str] = None
    quantity: Optional[int] = None
    batch: Optional[str] = None
    price: Optional[float] = None   # ← додано

class InventorySchema(InventoryBase):
    id: int

    class Config:
        orm_mode = True
