from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.schemas.database import Base

class Journal(Base):
    __tablename__ = "journal"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    operation = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)

    # зовнішній ключ для зв’язку з entry_lines
    entry_id = Column(Integer, ForeignKey("entry_lines.id"), nullable=True)

    # ORM‑зв’язок з EntryLine
    entry_line = relationship("EntryLine", back_populates="journal", lazy="joined")
