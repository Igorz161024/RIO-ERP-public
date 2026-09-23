from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Journal(Base):
    __tablename__ = "journal"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    operation = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    account = relationship("Account", back_populates="journals")

    # двосторонній зв’язок із EntryLine (рядкове ім’я, без імпорту)
    entry_lines = relationship(
        "EntryLine",
        back_populates="journal",
        cascade="all, delete-orphan"
    )
