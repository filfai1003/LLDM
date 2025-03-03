# repositories/ai_request_repository.py
from sqlalchemy.orm import Session
from src.models.ai_request_model import AIRequest
from src.schemas.ai_request_schemas import AIRequestCreate

def create_ai_request(db: Session, ai_request_data: AIRequestCreate) -> AIRequest:
    db_ai_request = AIRequest(
        input=ai_request_data.input,
        output=None,  # all'inizio NULL, verrà popolato dopo l'invocazione del modello
        model=ai_request_data.model,
        user_id=ai_request_data.user_id
    )
    db.add(db_ai_request)
    db.commit()
    db.refresh(db_ai_request)
    return db_ai_request

def get_ai_request_by_id(db: Session, request_id: int) -> AIRequest | None:
    return db.query(AIRequest).filter(AIRequest.id == request_id).first()

def update_ai_request_output(db: Session, request_id: int, output_text: str) -> AIRequest | None:
    db_request = get_ai_request_by_id(db, request_id)
    if db_request is None:
        return None
    db_request.output = output_text
    db.commit()
    db.refresh(db_request)
    return db_request

def get_ai_requests_by_user(db: Session, user_id: int) -> list[AIRequest]:
    return db.query(AIRequest).filter(AIRequest.user_id == user_id).all()
