from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class EntryLine(Base):
    __tablename__ = "entry_lines"

    id = Column(Integer, primary_key=True, index=True)
    journal_id = Column(Integer, ForeignKey("journal.id"), nullable=False)
    account = Column(String, nullable=False)
    debit = Column(Float, default=0)
    credit = Column(Float, default=0)

    # зв’язок назад до Journal
    journal = relationship("Journal", back_populates="entry_lines")
