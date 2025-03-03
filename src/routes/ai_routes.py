from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.schemas.ai_request_schemas import AIRequestCreate, AIRequestRead
from src.repositories.ai_request_repository import (
    create_ai_request,
    update_ai_request_output,
    get_ai_requests_by_user,
    get_ai_request_by_id
)
from src.services.ai_service import get_ai_response_llada
from src.config import AVAILABLE_MODELS
from src.repositories.user_repository import get_user_by_id, update_user_credits

router = APIRouter()

@router.post("/request", response_model=AIRequestRead)
def create_request(ai_req: AIRequestCreate, db: Session = Depends(get_db)):
    if ai_req.model not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model not available."
        )
    
    user = get_user_by_id(db, ai_req.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    model_cost = AVAILABLE_MODELS[ai_req.model]
    if user.credits < model_cost:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient credits."
        )
    
    update_user_credits(db, user.id, user.credits - model_cost)
    
    db_ai_request = create_ai_request(db, ai_req)
    return db_ai_request

@router.post("/invoke/{request_id}", response_model=AIRequestRead)
def invoke_request(request_id: int, db: Session = Depends(get_db)):
    db_ai_request = get_ai_request_by_id(db, request_id)
    if not db_ai_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI Request not found"
        )

    response_text = get_ai_response_llada(db_ai_request.input)

    updated_request = update_ai_request_output(db, db_ai_request.id, response_text)
    if not updated_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not update AI Request"
        )
    return updated_request

@router.get("/user/{user_id}", response_model=list[AIRequestRead])
def list_ai_requests_for_user(user_id: int, db: Session = Depends(get_db)):
    """
    Elenca tutte le richieste AI effettuate da uno specifico utente.
    """
    requests = get_ai_requests_by_user(db, user_id)
    return requests
