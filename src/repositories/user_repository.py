from sqlalchemy.orm import Session
from src.models.user_model import User
from src.schemas.user_schemas import UserCreate

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_create: UserCreate) -> User:
    db_user = User(
        name=user_create.name,
        email=user_create.email,
        password=user_create.password,  # TODO Encrypt the password in production
        credits=user_create.credits
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def update_user_credits(db: Session, user_id: int, new_credits: int) -> User:
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.credits = new_credits
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
