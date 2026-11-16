from backend.database import Base, engine
from backend.models import (
    accounts,
    journal,
    user,
    inventory,
    sales,
    purchases,
    legal,
    finance
)

def init_db():
    print("Creating tables in erp_diplom...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init_db()

