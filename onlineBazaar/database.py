from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def db_connect():
    create_url = "postgresql://postgres:sarneesh@localhost:5432/bazaar"
    db=create_engine(create_url)
    Session = sessionmaker(bind=db)
    session = Session()
    return (session)
