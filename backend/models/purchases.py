from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    supplier = Column(String, nullable=False)
    country = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
