from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Legal"])

class LegalDoc(BaseModel):
    doc_id: str
    title: str
    status: str

@router.get("/")
def get_legal_docs():
    return [
        {
            "doc_id": "L-001",
            "title": "Контракт з постачальником",
            "status": "Активний"
        }
    ]


