from pydantic import BaseModel
from typing import Optional

class AccountBase(BaseModel):
    name: str
    balance: float

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[float] = None

class AccountSchema(AccountBase):
    id: int

    class Config:
        orm_mode = True
