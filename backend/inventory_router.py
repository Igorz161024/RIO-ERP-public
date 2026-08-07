from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Inventory"])

class InventoryItem(BaseModel):
    product: str
    quantity: int
    batch: str

@router.get("/")
def get_inventory():
    return [
        {
            "product": "Ноутбук ASUS ZenBook",
            "quantity": 15,
            "batch": "2026-04-21"
        }
    ]


