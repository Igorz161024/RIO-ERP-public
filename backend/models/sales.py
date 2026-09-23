from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = {"extend_existing": True}  # дозволяє уникнути дублювання при повторному визначенні

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String, nullable=False)
    invoice = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
