from pydantic import BaseModel
from typing import Optional

class LegalBase(BaseModel):
    contract: str
    partner: str
    status: str

class LegalCreate(LegalBase):
    pass

class LegalUpdate(BaseModel):
    contract: Optional[str] = None
    partner: Optional[str] = None
    status: Optional[str] = None

class LegalSchema(LegalBase):
    id: int

    class Config:
        orm_mode = True
