# models/ai_request_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.models import Base

class AIRequest(Base):
    __tablename__ = "ai_requests"

    id = Column(Integer, primary_key=True, index=True)
    input = Column(Text, nullable=False)
    output = Column(Text, nullable=True)
    model = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Facoltativo: definisci una relazione per accedere ai dati dello user
    user = relationship("User", backref="ai_requests")
