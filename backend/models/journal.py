from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Journal(Base):
    __tablename__ = "journal"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    operation = Column(String, nullable=False)
    status = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account", back_populates="journals")
