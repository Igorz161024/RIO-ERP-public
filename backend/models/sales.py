from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    client = Column(String)
    invoice = Column(String)
    amount = Column(Float)
