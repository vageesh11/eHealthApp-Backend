from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL=os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    # return engine,SessionLocal,Base 