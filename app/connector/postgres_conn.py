
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def database_url():
    url=os.getenv("DATABASE_URL")
    engine = create_engine(url)

    SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

    Base = declarative_base()

    return engine,SessionLocal,Base 
    # return "database_url function to DB successfully created"