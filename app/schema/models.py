from sqlalchemy import Column, Integer, String
from app.connector.postgres_conn import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=False)
    password = Column(String,nullable=False) #hashed password
