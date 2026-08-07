from sqlalchemy import Column, Integer, String
from backend.database import Base

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    quantity = Column(Integer)
    batch = Column(String)
