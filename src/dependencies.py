# dependencies.py
from typing import Generator
from fastapi import Depends
from .config import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
