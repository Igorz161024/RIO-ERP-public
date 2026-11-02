from sqlalchemy import Column, Integer, String, Float
from backend.database import Base


class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    client = Column(String, nullable=False)

    product = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    amount = Column(Float, nullable=False)