from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
from backend.database import engine, SessionLocal
Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True)
    name = Column(String)
    type = Column(String)

class EntryLine(Base):
    __tablename__ = "entry_lines"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    debit = Column(Integer, default=0)
    credit = Column(Integer, default=0)
    account = relationship("Account")

def add_account(code, name, type):
    db = SessionLocal()
    account = db.query(Account).filter_by(code=code).first()
    if not account:
        account = Account(code=code, name=name, type=type)
        db.add(account)
        db.commit()
        db.refresh(account)
    db.close()
    return account

def add_entry(date, description, lines):
    db = SessionLocal()
    for line in lines:
        entry_line = EntryLine(account_id=line["account_id"], debit=line["debit"], credit=line["credit"])
        db.add(entry_line)
    db.commit()
    db.close()

def get_account_balance(account_id):
    db = SessionLocal()
    debit = sum(l.debit for l in db.query(EntryLine).filter_by(account_id=account_id))
    credit = sum(l.credit for l in db.query(EntryLine).filter_by(account_id=account_id))
    db.close()
    return debit - credit