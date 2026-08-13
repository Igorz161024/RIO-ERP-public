from sqlalchemy import Column, Integer, String
from backend.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    batch = Column(String, nullable=False)
