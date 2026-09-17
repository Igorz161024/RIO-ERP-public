from backend.database import SessionLocal
from backend.models.accounts import Account
from backend.models.entry_lines import EntryLine

def add_account(code: str, name: str, type: str):
    """Додати новий рахунок, якщо він ще не існує"""
    db = SessionLocal()
    account = db.query(Account).filter_by(code=code).first()
    if not account:
        account = Account(code=code, name=name, type=type)
        db.add(account)
        db.commit()
        db.refresh(account)
    db.close()
    return account

def add_entry(date, description, lines: list[dict]):
    """Створити проводки для операції"""
    db = SessionLocal()
    for line in lines:
        entry_line = EntryLine(
            journal_id=line["journal_id"],
            account=line["account"],
            debit=line.get("debit", 0),
            credit=line.get("credit", 0)
        )
        db.add(entry_line)
    db.commit()
    db.close()

def get_account_balance(account: str):
    """Розрахувати залишок по рахунку"""
    db = SessionLocal()
    debit = sum(l.debit for l in db.query(EntryLine).filter_by(account=account))
    credit = sum(l.credit for l in db.query(EntryLine).filter_by(account=account))
    db.close()
    return debit - credit
