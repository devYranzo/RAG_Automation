from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from routes import auth, index, search, system, file_manager, profile, users
from database.db import Base, engine
from database.seeders import run_seeders
from models.user import User
from models.profile import Profile

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await run_seeders()
    yield

app = FastAPI(
    title="TalentFinder API",
    lifespan=lifespan
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files mount
app.mount("/pdfs", StaticFiles(directory=settings.PDF_PATH), name="pdfs")

# Routes
app.include_router(auth.router)
app.include_router(index.router)
app.include_router(search.router)
app.include_router(system.router)
app.include_router(file_manager.router)
app.include_router(profile.router)
app.include_router(users.router)
