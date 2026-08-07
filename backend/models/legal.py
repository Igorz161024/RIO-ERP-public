from sqlalchemy import Column, Integer, String
from backend.database import Base

class Legal(Base):
    __tablename__ = "legal"
    id = Column(Integer, primary_key=True, index=True)
    contract = Column(String)
    partner = Column(String)
    status = Column(String)
