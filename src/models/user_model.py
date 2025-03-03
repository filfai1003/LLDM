from sqlalchemy import Column, Integer, String
from . import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    credits = Column(Integer, nullable=False, default=0)
    user_type = Column(String, nullable=False, default="base")
