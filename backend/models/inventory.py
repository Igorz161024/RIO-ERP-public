from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = {"extend_existing": True}  # уникнення дублювання

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    batch = Column(String, nullable=False)
    price = Column(Float, nullable=False)   # ← нове поле

