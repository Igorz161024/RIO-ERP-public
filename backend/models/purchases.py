from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Purchases(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    supplier = Column(String)
    country = Column(String)
    amount = Column(Float)
