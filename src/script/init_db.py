# scripts/init_db.py
from src.config import engine
from src.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database and tables created successfully!")
