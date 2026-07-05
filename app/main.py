from fastapi import FastAPI
from app.config import settings
from app.database import Base, engine
from app.models.user import User
from app.models.company import Company
from app.routers import auth
from app.routers import companies
from app.models.chat_memory import ChatMemory 
from app.routers import chat
from app.routers import prd
from app.models.prd import PRD
from app.routers import pitchdeck
from app.models.pitchdeck import PitchDeck

#Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(chat.router)
app.include_router(prd.router)
app.include_router(pitchdeck.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Solirna AI Backend!"
    }
