from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine

from app.models.user import User
from app.models.company import Company
from app.models.chat_memory import ChatMemory
from app.models.prd import PRD
from app.models.pitchdeck import PitchDeck

from app.routers import auth
from app.routers import companies
from app.routers import chat
from app.routers import prd
from app.routers import pitchdeck

# NEW
from app.services.qdrant_service import create_collection


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "https://solirnaai.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():

    # Create PostgreSQL tables
    Base.metadata.create_all(bind=engine)

    # Create Qdrant collection (runs only if it doesn't already exist)
    create_collection()


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
