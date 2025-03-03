# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import user_routes, ai_routes
from src.models import Base
from src.config import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea le tabelle
Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(ai_routes.router, prefix="/ai", tags=["AI Requests"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Large Language Diffusion Model API"}
