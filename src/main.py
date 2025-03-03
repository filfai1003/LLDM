import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import user_routes
from src.config import engine
from src.models import Base

# Create the FastAPI app
app = FastAPI(
    title="Large Language Diffusion Model API",
    description="API to use various AI models through purchasable credits",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific URLs in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Automatically create tables on app startup (optional)
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
// app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
// app.include_router(ai_routes.router, prefix="/ai", tags=["AI Services"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Large Language Diffusion Model API"}
