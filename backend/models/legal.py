from sqlalchemy import Column, Integer, String
from backend.database import Base

class Legal(Base):
    __tablename__ = "legal"

    id = Column(Integer, primary_key=True, index=True)
    contract = Column(String, nullable=False)
    partner = Column(String, nullable=False)
    status = Column(String, nullable=False)
