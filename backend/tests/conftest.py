import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import accounts, journal

@pytest.fixture(scope='module')
def db_session():
    engine = create_engine("postgresql://postgres:4568@localhost:5434/erp_diplom")
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
