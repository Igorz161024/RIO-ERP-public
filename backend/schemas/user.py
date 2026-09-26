from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True

