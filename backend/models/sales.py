from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String, nullable=False)
    invoice = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
