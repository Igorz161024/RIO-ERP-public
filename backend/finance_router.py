from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Finance"])

class FinanceEntry(BaseModel):
    date: str
    debit: str
    credit: str
    amount: int
    desc: str

@router.get("/")
def get_finance():
    return [
        {
            "date": "2026-04-21",
            "debit": "Склад",
            "credit": "Постачальник",
            "amount": 5000,
            "desc": "Імпорт товару"
        }
    ]


