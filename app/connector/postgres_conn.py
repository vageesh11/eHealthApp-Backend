from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from dotenv import load_dotenv
import os

# load_dotenv()

def database_url():
    url=os.getenv("DATABASE_URL")
    engine = create_engine(url)

    SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

    Base = declarative_base()

    return engine,SessionLocal,Base 