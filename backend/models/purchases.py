from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class Purchase(Base):
    __tablename__ = "purchases"
    __table_args__ = {"extend_existing": True}  # дозволяє уникнути дублювання при повторному визначенні

    id = Column(Integer, primary_key=True, index=True)
    supplier = Column(String, nullable=False)
    country = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
