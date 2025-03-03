from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import user_routes
from src.config import engine
from src.models import Base

# Crea l'app FastAPI
app = FastAPI(
    title="Large Language Diffusion Model API",
    description="API per utilizzare diversi modelli di IA tramite crediti acquistabili",
    version="1.0.0"
)

# Configura il middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia con gli URL specifici in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creiamo le tabelle in modo automatico all'avvio dell'app (opzionale)
Base.metadata.create_all(bind=engine)

# Includi le rotte
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
# app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
# app.include_router(ai_routes.router, prefix="/ai", tags=["AI Services"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Large Language Diffusion Model API"}
