from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from backend.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    balance = Column(Float, default=0)

    journals = relationship("Journal", back_populates="account")
