from pydantic import BaseModel
from typing import Optional

class InventoryBase(BaseModel):
    product: str
    quantity: int
    batch: str

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    product: Optional[str] = None
    quantity: Optional[int] = None
    batch: Optional[str] = None

class InventorySchema(InventoryBase):
    id: int

    class Config:
        from_attributes = True
