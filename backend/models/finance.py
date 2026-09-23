from sqlalchemy import Column, Integer, String, Float, Date
from backend.database import Base

class Finance(Base):
    __tablename__ = "finance"
    __table_args__ = {"extend_existing": True}  # дозволяє уникнути дублювання при повторному визначенні

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    account = Column(String, index=True, nullable=False)
    debit = Column(Float, default=0.0)
    credit = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)
    description = Column(String, nullable=True)
